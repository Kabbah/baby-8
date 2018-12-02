#include <SoftwareSerial.h>
#include <Ultrasonic.h>

// Comando para ler o ultrassônico (enviado pelo RPi)
#define SEND_SENSOR_VAL_COMMAND 'S'

// Define os pinos para o ultrassônico
#define US_TRIGGER_PIN 4
#define US_ECHO_PIN    5

// Define os pinos para a serial da placa de Bluetooth
#define BT_RX_PIN      10
#define BT_TX_PIN      11

// Instancia a serial do Bluetooth
SoftwareSerial btSerial(BT_RX_PIN, BT_TX_PIN); // RX, TX

// Instancia o ultrassônico
Ultrasonic ultrasonic(US_TRIGGER_PIN, US_ECHO_PIN);

// LED (debug)
#define LED_PIN 13
bool ledOn = false;

// Comando
char recvCommand = 0;
    
void setup() {
    // Inicia a serial
    Serial.begin(115200);
    // Inicia a serial configurada nas portas 10 e 11
    btSerial.begin(9600);

    // LED
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW);
    randomSeed(analogRead(0));
}

void loop() {
    // Lê o Bluetooth se tiver algum dado para ler
    if (btSerial.available()) {
        char cmd = btSerial.read();

        if (cmd == SEND_SENSOR_VAL_COMMAND) {
            long usMicrosec = ultrasonic.timing();
            float distance = ultrasonic.convert(usMicrosec, Ultrasonic::CM);

            btSerial.print(distance);
            Serial.println(distance); // FIXME: DEBUG

            ledOn = !ledOn;
            if (ledOn) digitalWrite(LED_PIN, HIGH);
            else digitalWrite(LED_PIN, LOW);
        }
    }
}

