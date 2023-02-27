<?php

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Headers: Content-Type');

require 'PHPMailer/src/Exception.php';
require 'PHPMailer/src/PHPMailer.php';
require 'PHPMailer/src/SMTP.php';

// Переменные, которые отправляет пользователь

$sitename = 'bibliodev.ru';
$from = 'thesuperuserstyle@gmail.com'; //'info@bibliodev.ru';
$to = 'yaonkey@gmail.com';

$name = $_POST['name'];
$email = $_POST['email'];
$message = $_POST['message'];
$salary = $_POST['salary'];
$position = $_POST['position'];
$experience = $_POST['experience'];
$type = $_POST['type'];
$file = $_FILES['file'];

$company = $_POST['company'] ?: null;
$info = $_POST['info'] ?: null;
$phone = $_POST['phone'] ?: null;
$interested = $_POST['interested'] ?: null;
$budget = $_POST['budget'] ?: null;

// Формирование письма с резюме
if (empty($company)){
  $title = "Резюме - Письмо с сайта bibliodev.ru";

  $body = "<h2>Новое письмо c сайта bibliodev.ru - Резюме</h2>";
  $body .= "<p>";
  $body .= "<b>Имя:</b> $name<br>";
  $body .= "<b>Почта:</b> $email<br>";
  $body .= "<b>Позиция:</b> $position<br>";
  $body .= "<b>Опыт работы:</b> $experience<br>";
  $body .= "<b>Тип работы:</b> $type<br>";
  $body .= "<b>Ожидаемая зарплата:</b> $salary<br>";
  $body .= "<b>Сообщение:</b><br>$message<br>";
  $body .= "</p>";
} else { // Формирование письма без резюме
  $title = "Обратная связь - Письмо с сайта bibliodev.ru";

  $body = "<h2>Новое письмо c сайта bibliodev.ru - Обратная связь</h2>";
  $body .= "<p>";
  $body .= "<b>Имя:</b> $name<br>";
  $body .= "<b>Компания:</b> $company<br>";
  $body .= "<b>Интересует:</b> $interested<br>";
  $body .= "<b>Информация:</b> $info<br>";
  $body .= "<b>Бюджет:</b> $budget<br>";
  $body .= "<b>Почта:</b> $email<br>";
  $body .= "<b>Телефон:</b> $phone<br>";
  $body .= "</p>";
}

$mail = new PHPMailer(true);

try {
  $mail->setFrom($from, $sitename); // Адрес самой почты и имя отправителя
  $mail->addAddress($to);

  // Прикрипление файлов к письму todo
  if (!empty($file['name'][0])) {
    for ($ct = 0; $ct < count($file['tmp_name']); $ct++) {
      $uploadfile = tempnam(sys_get_temp_dir(), sha1($file['name'][$ct]));
      $filename = $file['name'][$ct];
      if (move_uploaded_file($file['tmp_name'][$ct], $uploadfile)) {
        $mail->addAttachment($uploadfile, $filename);
        $rfile[] = "Файл $filename прикреплён";
      } else {
        $rfile[] = "Не удалось прикрепить файл $filename";
      }
    }
  }

  // Отправка сообщения
  $mail->isHTML(true);
  $mail->Subject = $title;
  $mail->Body = $body;

  // Проверяем отравленность сообщения
  if ($mail->send()) {
    $result = "success";
  } else {
    $result = "error";
  }

} catch (Exception $e) {
  $result = "error";
  $status = "Сообщение не было отправлено. Причина ошибки: {$mail->ErrorInfo}";
}

// Отображение результата
echo json_encode(["result" => $result, "resultfile" => $rfile, "status" => $status]);
