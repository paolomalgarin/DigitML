<?php
// image_predict.php
header('Content-Type: application/json');


if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $logFile = __DIR__ . '/imageStore.json';
    if (!file_exists($logFile)) {
        echo json_encode([]);
        exit;
    }

    $content = file_get_contents($logFile);
    $data = json_decode($content, true);
    if (!is_array($data)) {
        echo json_encode([]);
        exit;
    }

    echo json_encode($data);
    exit;
}


function sendToML(string $imageBase64, string $endpoint): array {
    $url = 'http://' . $_SERVER['HTTP_HOST']
         . str_replace('API/image.php',
                       'NeuralNetwork/predict' . ($endpoint === 'number' ? 'Digits' : 'Letters') . '.php',
                       $_SERVER['REQUEST_URI']
                 );
    $payload = json_encode(['image' => 'data:image/png;base64,' . $imageBase64]);
    $opts = [
        'http' => [
            'header'       => "Content-Type: application/json\r\n",
            'method'       => 'POST',
            'content'      => $payload,
            'ignore_errors'=> true,
        ],
    ];
    $ctx      = stream_context_create($opts);
    $resp     = @file_get_contents($url, false, $ctx);
    if ($resp === false) {
        return ['error' => 'HTTP request failed'];
    }
    if (strpos($resp, 'Errore PNG:') !== false) {
        return ['error' => $resp];
    }
    return json_decode($resp, true) ?: ['error' => "Invalid JSON response (resp: $resp, data:image/png;base64,$imageBase64)"];
}

//
// 1) Lettura input JSON e base64
//
$raw   = file_get_contents('php://input');
$data  = json_decode($raw, true);
if (empty($data['image'])) {
    echo json_encode(['error' => 'Nessuna immagine inviata']);
    exit;
}
$endpoint = $data['endpoint'] ?? 'number';
$img64    = $data['image'];
if (strpos($img64, 'base64,') !== false) {
    $img64 = substr($img64, strpos($img64, 'base64,') + 7);
}
$imgData = base64_decode($img64, true);
if ($imgData === false) {
    echo json_encode(['error' => 'Base64 non valido']);
    exit;
}

//
// 2) Creazione risorsa GD e preprocessing
//
$src = @imagecreatefromstring($imgData);
if (! $src) {
    echo json_encode(['error' => 'Immagine sorgente non valida']);
    exit;
}

// scala di grigi + negativo
$w    = imagesx($src);
$h    = imagesy($src);
$gray = imagecreatetruecolor($w, $h);
imagecopy($gray, $src, 0, 0, 0, 0, $w, $h);
imagedestroy($src);

// ridimensiona 28×28
$resized = imagescale($gray, 28, 28, IMG_NEAREST_NEIGHBOUR);
imagedestroy($gray);

// 3) Costruisci un canvas truecolor 28×28
$output = imagecreatetruecolor(28, 28);
imagealphablending($output, false);
imagesavealpha($output, false);

for ($x = 0; $x < 28; $x++) {
    for ($y = 0; $y < 28; $y++) {
        $idx       = imagecolorat($resized, $x, $y);
        $c         = imagecolorsforindex($resized, $idx);
        $grayValue = (int)(($c['red'] + $c['green'] + $c['blue']) / 3);
        // crea il colore RGB=grayValue
        $col = ($grayValue << 16) | ($grayValue << 8) | $grayValue;
        imagesetpixel($output, $x, $y, $col);
    }
}
imagedestroy($resized);

//
// 4) Esporta PNG con filtro NONE (0)
//
// Nota: usiamo PNG_FILTER_NONE per garantire che la prima byte di ogni scanline
// sia 0, così il tuo parser non rifiuta “Filtro PNG 1 non supportato”.
//
ob_start();
imagepng($output, null, 0, PNG_FILTER_NONE);
$pngBlob = ob_get_clean();
imagedestroy($output);

//
// 5) Invio al server di inferenza
//
$base64Out  = base64_encode($pngBlob);
$prediction = sendToML($base64Out, $endpoint);
//
// 6.1) Salvataggio nel file imageStore.json
//
$logFile = __DIR__ . '/imageStore.json';

// Crea struttura iniziale se il file non esiste o è malformato
$logData = [];
if (file_exists($logFile)) {
    $contents = file_get_contents($logFile);
    $logData = json_decode($contents, true);
    if (!is_array($logData)) {
        $logData = [];
    }
}

// Aggiungi nuova entry
$logData[] = [
    'image'      => 'data:image/png;base64,' . $base64Out,
    'prediction' => $prediction['prediction'] ?? $prediction, // fallback in caso di errore
    'date'       => date('d/m/Y H:i'),
];

// Mantieni solo le ultime 50
if (count($logData) > 50) {
    $logData = array_slice($logData, -50);
}

// Salva di nuovo nel file
file_put_contents($logFile, json_encode($logData, JSON_PRETTY_PRINT));


// 6) Output JSON finale
// echo $base64Out;
echo json_encode($prediction);
