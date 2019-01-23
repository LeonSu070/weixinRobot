<?php
function getReqSign($params, $appkey)
{
    ksort($params);
    $str = '';
    foreach ($params as $key => $value)
    {
        if ($value !== '')
        {
            $str .= $key . '=' . urlencode($value) . '&';
        }
    }

    $str .= 'app_key=' . $appkey;
    echo $str . "\n";
    $sign = strtoupper(md5($str));
    return $sign;
}

function doHttpPost($url, $params)
{
    $curl = curl_init();

    $response = false;
    do
    {
        // 1. è¾ç®HTTP URL (APIå°å)
        curl_setopt($curl, CURLOPT_URL, $url);

        // 2. è¾ç®HTTP HEADER (è¨åPOST)
        $head = array(
            'Content-Type: application/x-www-form-urlencoded'
        );
        curl_setopt($curl, CURLOPT_HTTPHEADER, $head);

        // 3. è¾ç®HTTP BODY (URLé®å¼å¹)
        $body = http_build_query($params);
        curl_setopt($curl, CURLOPT_POST, true);
        curl_setopt($curl, CURLOPT_POSTFIELDS, $body);

        // 4. èç¨APIïè·åååçæ
        curl_setopt($curl, CURLOPT_HEADER, false);
        curl_setopt($curl, CURLOPT_NOBODY, false);
        curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($curl, CURLOPT_SSL_VERIFYHOST, true);
        curl_setopt($curl, CURLOPT_SSL_VERIFYPEER, false);
        $response = curl_exec($curl);
        if ($response === false)
        {
            $response = false;
            break;
        }

        $code = curl_getinfo($curl, CURLINFO_HTTP_CODE);
        if ($code != 200)
        {
            $response = false;
            break;
        }
    } while (0);

    curl_close($curl);
    return $response;
}


$appkey="Iq7ff66Bp4I9RYGR";
$params = array(
    'app_id'     => '2111653146',
    'session'    => '7648242348208408208',
    'question'   => 'how are you doing',
    'time_stamp' => strval(time()),
    'nonce_str'  => strval(rand()),
    'sign'       => '',
);
$params['sign'] = getReqSign($params, $appkey);
var_dump($params);
$url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat';
$response = doHttpPost($url, $params);
echo $response;
