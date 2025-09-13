#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

// ---- WiFi ----
const char* ssid = "su_usuario";
const char* password = "su_contraseña";

// ---- Servidor FastAPI ----
const char* serverUrl = "server_url";

const int PIN_SOIL_ADC = 34;   // HL-69 AO
const int PIN_TRIG     = 33;   // HC-SR04 TRIG
const int PIN_ECHO     = 35;   // HC-SR04 ECHO (usar divisor 5V->3.3V)
const int RELAY1       = 25;   // Riego
const int RELAY2       = 26;   // Llenado
const int LED_VENT     = 27;   // Ventilador (LED)
const int PIN_DHT      = 32;   // DHT11
const int PIN_PIR      = 13;   // PIR
const int PIN_MQ2      = 12;   // MQ2 (DO digital)

DHT dht(PIN_DHT, DHT11);

void setup() {
  Serial.begin(115200);

    WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");
  Serial.println(WiFi.localIP());

  // Pines salida
  pinMode(RELAY1, OUTPUT);
  pinMode(RELAY2, OUTPUT);
  pinMode(LED_VENT, OUTPUT);

  // Pines entrada
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);
  pinMode(PIN_PIR, INPUT);
  pinMode(PIN_MQ2, INPUT);

  dht.begin();
}

// ---- Funciones auxiliares ----
long medirDistancia() {
  digitalWrite(PIN_TRIG, LOW);
  delayMicroseconds(2);
  digitalWrite(PIN_TRIG, HIGH);
  delayMicroseconds(10);
  digitalWrite(PIN_TRIG, LOW);
  long duracion = pulseIn(PIN_ECHO, HIGH);
  return duracion * 0.034 / 2; // cm
}


void loop() {
  // Declaración de doc al principio de loop()
  StaticJsonDocument<256> doc;

  // Lecturas
  int soilValue = analogRead(PIN_SOIL_ADC);
  long dist_cm = medirDistancia();

  // Leer temperatura y humedad
  float temperatura = dht.readTemperature();
  float humedad = dht.readHumidity();

    if (isnan(temperatura) || isnan(humedad)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    doc["temp"] = (const char*)NULL;
    doc["humedad"] = (const char*)NULL;
  } else {
    Serial.print(F("Temperature: "));
    Serial.print(temperatura);
    Serial.print(F("°C, Humidity: "));
    Serial.print(humedad);
    Serial.println(F("%"));

    doc["temp"] = temperatura;
    doc["humedad"] = humedad;
  }

  int pirValue = digitalRead(PIN_PIR);
  int mq2Value = digitalRead(PIN_MQ2);

  // Lógicas simples
  int riego = soilValue > 3000 ? 1 : 0;
  int llenado = dist_cm > 10 ? 1 : 0;
  int vent = (!isnan(temperatura) && temperatura > 28) ? 1 : 0;

  // Salidas físicas
  digitalWrite(RELAY1, !riego); 
  digitalWrite(RELAY2, !llenado);
  digitalWrite(LED_VENT, vent);


    doc["soil"] = soilValue;
    doc["dist_cm"] = dist_cm;
    doc["riego"] = riego;
    doc["llenado"] = llenado;
    doc["vent"] = vent;
    doc["pir"] = pirValue;
    doc["mq2"] = mq2Value;

  String json;
  serializeJson(doc, json);

  Serial.print("Enviando JSON -> ");
  Serial.println(json);

  // ---- Enviar POST ----
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    int httpResponseCode = http.POST(json);

    if (httpResponseCode > 0) {
      Serial.print("POST OK (");
      Serial.print(httpResponseCode);
      Serial.println(")");
      Serial.println(http.getString());
    } else {
      Serial.print("Error en POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }

  delay(10000); 
}