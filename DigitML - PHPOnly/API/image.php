<?php
// image_predict.php
header('Content-Type: text/html');

function sendToML($imageBase64, $endpoint)
{
    $url = 'http://' . $_SERVER['HTTP_HOST'] . str_replace('API/image.php', 'NeuralNetwork/predict' . ($endpoint == 'number' ? 'Digits' : 'Letters') . '.php', $_SERVER['REQUEST_URI']);
    // echo $url;
    $payload = json_encode(['image' => 'data:image/png;base64,' . $imageBase64]);

    // echo $payload;

    $options = [
        'http' => [
            'header'  => "Content-Type: application/json\r\n",
            'method'  => 'POST',
            'content' => $payload,
            'ignore_errors' => true
        ]
    ];

    try {
        $context = stream_context_create($options);
        $response = file_get_contents($url, false, $context);

        // Controlla se la risposta contiene un errore PNG
        if (strpos($response, 'Errore PNG:') !== false) {
            return ['error' => $response];
        }

        return json_decode($response, true) ?? ['error' => 'Risposta non valida: ' . $response];
    } catch (Exception $e) {
        return ['error' => $e->getMessage()];
    }
}

$data = json_decode(file_get_contents('php://input'), true);
$endpoint = $data['endpoint'];

// Estrai e decodifica immagine
$imageParts = explode(',', $data['image']);
$base64 = end($imageParts);
$imageData = base64_decode($base64);

if ($imageData) {
    // Processa immagine// Modifica la sezione di processing
    $src = imagecreatefromstring($imageData);

    // Crea immagine in scala di grigi
    $gray = imagecreatetruecolor(imagesx($src), imagesy($src));
    imagecopy($gray, $src, 0, 0, 0, 0, imagesx($src), imagesy($src));
    imagetruecolortopalette($gray, false, 256);

    // Inverti colori se necessario
    imagefilter($gray, IMG_FILTER_NEGATE);

    // Ridimensiona
    $resized = imagescale($gray, 28, 28);
    imagedestroy($gray);

    // Salva l'immagine con impostazioni specifiche
    // Modifica la sezione di salvataggio dell'immagine
    ob_start();
    // Forza l'uso di PNG 8-bit colortype 0 (grayscale) e disabilita filtri
    $grayscale = imagecreatetruecolor(28, 28);
    imagepalettecopy($grayscale, $resized);
    imagepng($grayscale, null, 0, PNG_NO_FILTER);
    imagedestroy($grayscale);
    $resizedImage = ob_get_clean();
    $resizedBase64 = base64_encode($resizedImage);


    // Invia al ML
    $prediction = sendToML($resizedBase64, $endpoint);

    
    echo json_encode($prediction);

    imagedestroy($src);
    imagedestroy($resized);
}
