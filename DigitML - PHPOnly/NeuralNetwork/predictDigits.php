<?php
require __DIR__ . '/vendor/autoload.php';
use OnnxRuntime\Model;

// 1) Leggi il JSON dal body della richiesta
$json = file_get_contents('php://input');
$data = json_decode($json, true);
$base64 = $data['image'] ?? '';

if (!$base64) {
    http_response_code(400);
    echo json_encode(['error' => 'Nessuna immagine inviata']);
    exit;
}

if (strpos($base64, 'base64,') !== false) {
    $base64 = substr($base64, strpos($base64, 'base64,') + 7);
}

$imageData = base64_decode($base64, true);
if ($imageData === false) {
    http_response_code(400);
    echo json_encode(['error' => 'Base64 non valido']);
    exit;
}

// 2) Decodifica PNG/JPEG/GIF con GD
$im = @imagecreatefromstring($imageData);
if (!$im) {
    http_response_code(400);
    echo json_encode(['error' => 'Impossibile caricare l\'immagine']);
    exit;
}

// 3) Ridimensiona a 28×28 (se necessario per il modello MNIST)
$thumb = imagescale($im, 28, 28, IMG_NEAREST_NEIGHBOUR);
imagedestroy($im);
$w = imagesx($thumb);
$h = imagesy($thumb);

// 4) Costruisci il feed array NHWC: [batch=1][height=28][width=28][channels=1]\$tensor = [];
for ($y = 0; $y < $h; $y++) {
    $rowChannels = [];
    for ($x = 0; $x < $w; $x++) {
        $rgb = imagecolorat($thumb, $x, $y);
        $r   = ($rgb >> 16) & 0xFF;
        $g   = ($rgb >> 8)  & 0xFF;
        $b   = $rgb & 0xFF;
        $gray = ($r + $g + $b) / 3;
        // ogni pixel come vettore di canale singolo
        $rowChannels[] = [$gray / 255.0];
    }
    $tensor[] = $rowChannels;
}
imagedestroy($thumb);

$inputFeed = [
    'input_image' => [ $tensor ]  // batch dimension
];

// 5) Inferenza ONNX
$model  = new Model(__DIR__ . '/digits_model.onnx');
$result = $model->predict($inputFeed);

// 6) Estrai la classe con probabilità massima
$subArray = $result['output_class'][0];
$maxKey = array_search(max($subArray), $subArray);

// 7) Restituisci la risposta JSON
header('Content-Type: application/json');
echo json_encode(['prediction' => intval($maxKey)]);
