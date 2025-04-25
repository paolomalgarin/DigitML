<?php
require __DIR__ . '/vendor/autoload.php';
use OnnxRuntime\Model;

// 1) Prendi la stringa Base64 (eventuale Data-URI prefix incluso)
// Leggi il corpo JSON della richiesta
$json = file_get_contents('php://input');
$data = json_decode($json, true);
$base64 = $data['image'] ?? '';
if (!$base64) {
    die('Nessuna immagine inviata');
}
if (strpos($base64, 'base64,') !== false) {
    $base64 = substr($base64, strpos($base64, 'base64,') + 7);
}
$data = base64_decode($base64, true);
if ($data === false) {
    die('Base64 non valido');
}

// 2) Parser PNG che supporta colortype 0 (grayscale) e 2 (RGB)
function parsePngToGray(string $data): array
{
    if (substr($data, 0, 8) !== "\x89PNG\x0D\x0A\x1A\x0A") {
        throw new Exception('Non è un PNG valido');
    }
    $offset   = 8;
    $idatData = '';
    $width = $height = $bitDepth = $colorType = null;

    while ($offset < strlen($data)) {
        $len   = unpack('N', substr($data, $offset, 4))[1];
        $type  = substr($data, $offset + 4, 4);
        $chunk = substr($data, $offset + 8, $len);

        if ($type === 'IHDR') {
            $ihdr = unpack('Nwidth/Nheight/CbitDepth/CcolorType', $chunk);
            $width     = $ihdr['width'];
            $height    = $ihdr['height'];
            $bitDepth  = $ihdr['bitDepth'];
            $colorType = $ihdr['colorType'];
            if ($bitDepth !== 8 || !in_array($colorType, [0, 2], true)) {
                throw new Exception('Supportati solo PNG 8-bit colortype 0 o 2');
            }
        }

        if ($type === 'IDAT') {
            $idatData .= $chunk;
        }

        if ($type === 'IEND') {
            break;
        }

        // salta chunk: 4(len)+4(type)+len+4(CRC)
        $offset += 8 + $len + 4;
    }

    if (!$width || !$idatData) {
        throw new Exception('Chunk IHDR o IDAT mancanti');
    }

    $imgData = zlib_decode($idatData);
    if ($imgData === false) {
        throw new Exception('Decompressione IDAT fallita');
    }

    // 3) Estrai scanline per scanline (filtro 0)
    $pixels = [];
    $pos    = 0;
    for ($y = 0; $y < $height; $y++) {
        $filter = ord($imgData[$pos++]);
        if ($filter !== 0) {
            throw new Exception("Filtro PNG {$filter} non supportato");
        }
        $row = [];
        if ($colorType === 0) {
            // un byte per pixel
            for ($x = 0; $x < $width; $x++) {
                $row[] = ord($imgData[$pos++]);
            }
        } else {
            // RGB: tre byte per pixel
            for ($x = 0; $x < $width; $x++) {
                $r = ord($imgData[$pos++]);
                $g = ord($imgData[$pos++]);
                $b = ord($imgData[$pos++]);
                // converto in scala di grigi
                $gray = (int) round(0.299 * $r + 0.587 * $g + 0.114 * $b);
                $row[] = $gray;
            }
        }
        $pixels[] = $row;
    }

    return compact('width', 'height', 'pixels');
}

try {
    $png = parsePngToGray($data);
} catch (Exception $e) {
    die('Errore PNG: ' . $e->getMessage());
}

// 4) Costruisci il tensore [1,28,28,1] normalizzato
$inputTensor = [];
for ($y = 0; $y < $png['height']; $y++) {
    for ($x = 0; $x < $png['width']; $x++) {
        $inputTensor[0][$y][$x][0] = $png['pixels'][$y][$x] / 255.0;
    }
}

// 5) Inferenza con ONNX Runtime
$model  = new Model(__DIR__ . '/digits_model.onnx');
$result = $model->predict([
    'input_image' => $inputTensor
]);

// 6) Output JSON
header('Content-Type: application/json');
//prendo il valore max
$subArray = $result['output_class'][0];
$maxKey = array_search(max($subArray), $subArray);
//lo mando
echo "{ \"prediction\": $maxKey }";
