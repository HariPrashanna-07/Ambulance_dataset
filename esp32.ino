// AutoSignal - ESP32 4-road traffic controller (Serial / UART)
// Commands from Python (one character):
//   '1'..'4' -> ambulance on that road: it gets GREEN, all others RED
//   '0'      -> back to normal cycle
// If no ambulance command arrives for EMERGENCY_TIMEOUT ms, it returns to normal (fail-safe).

const int R[4] = {13, 26, 32, 21};   // red pins   (Road 1..4)
const int Y[4] = {14, 25, 23, 19};   // yellow pins
const int G[4] = {27, 33, 22, 18};   // green pins

const unsigned long GREEN_MS = 5000, YELLOW_MS = 1500, EMERGENCY_TIMEOUT = 10000;

int emergencyRoad = -1;              // -1 = normal mode
int current = 0;                     // road currently served in normal mode
bool yellowPhase = false;
unsigned long phaseStart = 0, lastCmd = 0;

void allRed() {
  for (int i = 0; i < 4; i++) {
    digitalWrite(R[i], HIGH); digitalWrite(Y[i], LOW); digitalWrite(G[i], LOW);
  }
}

void show(int road, bool yellow) {
  allRed();
  digitalWrite(R[road], LOW);
  digitalWrite(yellow ? Y[road] : G[road], HIGH);
}

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < 4; i++) { pinMode(R[i], OUTPUT); pinMode(Y[i], OUTPUT); pinMode(G[i], OUTPUT); }
  show(0, false);
  phaseStart = millis();
}

void loop() {
  // 1) read command from Python
  while (Serial.available()) {
    char c = Serial.read();
    if (c >= '1' && c <= '4') {
      emergencyRoad = c - '1';
      lastCmd = millis();
      show(emergencyRoad, false);
      Serial.println("EMERGENCY road " + String(emergencyRoad + 1));
    } else if (c == '0') {
      emergencyRoad = -1;
      phaseStart = millis();
      show(current, false);
      Serial.println("NORMAL");
    }
  }

  // 2) emergency mode: hold green, fail-safe timeout
  if (emergencyRoad >= 0) {
    if (millis() - lastCmd > EMERGENCY_TIMEOUT) {
      emergencyRoad = -1; phaseStart = millis(); show(current, false);
    }
    return;
  }

  // 3) normal cycle
  unsigned long now = millis();
  if (!yellowPhase && now - phaseStart > GREEN_MS) {
    yellowPhase = true; phaseStart = now; show(current, true);
  } else if (yellowPhase && now - phaseStart > YELLOW_MS) {
    yellowPhase = false; phaseStart = now;
    current = (current + 1) % 4; show(current, false);
  }
}
