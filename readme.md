# Mikroprocesorowy Regulator Temperatury PID (STM32)

**Przedmiot:** Systemy Mikroprocesorowe

**Cel:** Zaprojektowanie i implementacja układu sterowania temperaturą z wykorzystaniem algorytmu PID, wizualizacji danych i komunikacji szeregowej.

## 🎥 Prezentacja wideo

[Link do filmu na YouTube](https://www.youtube.com/watch?v=wEF-WTK1dMs)

## 📋 Spis treści

- [Opis projektu](#opis-projektu)
- [Funkcjonalności](#funkcjonalności)
- [Wykorzystane komponenty](#wykorzystane-komponenty)
- [Konfiguracja sprzętowa (Pinout)](#konfiguracja-sprzętowa-pinout)
- [Algorytm sterowania (PID)](#algorytm-sterowania-pid)
- [Instrukcja obsługi](#instrukcja-obsługi)
- [Wizualizacja i Telemetria](#wizualizacja-i-telemetria)
- [Wyniki i Charakterystyka](#wyniki-i-charakterystyka)

## 📝 Opis projektu

Projekt realizuje układ zamkniętej pętli regulacji temperatury przy użyciu mikrokontrolera z rodziny STM32. System odczytuje temperaturę otoczenia za pomocą czujnika BMP280, a następnie steruje elementem grzejnym (rezystorem) w celu osiągnięcia i utrzymania zadanej wartości (Set Point).

### Wymagania projektu

Projekt spełnia wymagania minimalne oraz rozszerzone:

- ✅ Realizacja algorytmu PID w czasie rzeczywistym
- ✅ Dwukierunkowa komunikacja UART (odbieranie komend i wysyłanie telemetrii)
- ✅ Obsługa lokalnego interfejsu: Enkoder obrotowy oraz wyświetlacz LCD 2x16

## 🚀 Funkcjonalności

### 🔍 Pomiar

- Odczyt temperatury z czujnika BMP280 (Interfejs I2C)

### 🎛️ Sterowanie

- Algorytm PID sterujący czasem włączenia grzałki (Time Proportional Control) w cyklu 1-sekundowym

### 👆 Interfejs użytkownika (HMI)

- Wyświetlanie temperatury zadanej i aktualnej na LCD
- Zmiana temperatury zadanej za pomocą enkodera obrotowego

### 📡 Komunikacja (UART)

- Wysyłanie danych w formacie tekstowym do rysowania wykresów (np. w Telemetry Viewer)
- Zdalna korekta temperatury zadanej za pomocą komend `+` / `-`

## 🛠 Wykorzystane komponenty

Zgodnie z założeniami projektowymi:

| Komponent              | Model/Opis                                         | Funkcja                        |
| ---------------------- | -------------------------------------------------- | ------------------------------ |
| **Mikrokontroler**     | STM32 (Zestaw Nucleo)                              | Główny jednostka sterująca     |
| **Czujnik**            | BMP280 (Temperatura/Ciśnienie)                     | Pomiar temperatury             |
| **Wyświetlacz**        | LCD 2x16 ze sterownikiem I2C (HD44780 + PCF8574)   | Interfejs użytkownika          |
| **Sterowanie**         | Enkoder inkrementalny                              | Ustawianie temperatury zadanej |
| **Element wykonawczy** | Grzałka (rezystor mocy) sterowana przez tranzystor | Element grzejny                |
| **Sygnalizacja**       | Dioda LED                                          | Sygnalizacja grzania           |

## 🔌 Konfiguracja sprzętowa (Pinout)

| Peryferium           | Pin / Port    | Funkcja                        |
| -------------------- | ------------- | ------------------------------ |
| **Grzałka (Heater)** | PD7           | Wyjście sterujące (PWM/On-Off) |
| **BMP280**           | I2C1          | Komunikacja z czujnikiem       |
| **LCD 2x16**         | I2C4          | Wyświetlacz                    |
| **Enkoder**          | TIM1          | Ustawianie temperatury zadanej |
| **UART**             | USART3        | Komunikacja z PC (115200 baud) |
| **LED Status**       | LD1_Pin (PB0) | Sygnalizacja włączenia grzałki |

## 🎛 Algorytm sterowania (PID)

W projekcie zaimplementowano dyskretny regulator PID wg wzoru:

```
u(t) = Kp·e(t) + Ki·∫e(t)dt + Kd·de(t)/dt
```

### Parametry strojenia (nastawy)

W kodzie zdefiniowano strukturę `PID_Controller` z następującymi wartościami:

| Parametr | Wartość | Opis                       |
| -------- | ------- | -------------------------- |
| **Kp**   | 400.0   | Wzmocnienie proporcjonalne |
| **Ki**   | 10.0    | Wzmocnienie całkujące      |
| **Kd**   | 50.0    | Wzmocnienie różniczkujące  |

### Ograniczenia wyjścia (Clamp)

Sygnał sterujący jest ograniczony do zakresu 0 - 1000. Wartość ta jest mapowana bezpośrednio na czas włączenia grzałki w milisekundach (w pętli 1-sekundowej).

```c
// Fragment implementacji sterowania czasem (Time Proportional Control)
int32_t heating_time = (int32_t)pid_output; // 0 do 1000 ms
int32_t cooling_time = 1000 - heating_time;
```

## 📖 Instrukcja obsługi

### 🚀 Uruchomienie

Po podłączenia zasilania, na ekranie LCD pojawi się komunikat powitalny, a następnie aktualna temperatura i temperatura zadana (T_zad).

### 🎛️ Zmiana temperatury (Lokalnie)

Obracaj enkoderem, aby zwiększyć lub zmniejszyć zadaną temperaturę.

### 📡 Zmiana temperatury (Zdalnie)

1. Otwórz terminal portu szeregowego
2. Ustawienia: 115200 baud, 8N1
3. Wyślij znak `+` aby zwiększyć offset temperatury lub `-` aby zmniejszyć

### 💡 Sygnalizacja

Dioda LED oraz pin PD7 są w stanie wysokim, gdy regulator dostarcza ciepło do układu.

## 📊 Wizualizacja i Telemetria

Mikrokontroler wysyła dane na port UART w formacie tekstowym, co ułatwia ich parsowanie przez programy typu Telemetry Viewer lub Serial Plotter.

### Przykład danych

```
26.50 27.00
26.62 27.00
26.80 27.00
```

Pozwala to na wykreślenie charakterystyki skokowej i zbadanie uchybu regulacji w czasie rzeczywistym.

## 📈 Wyniki i Charakterystyka

### Charakterystyka skokowa regulatora PID

![Charakterystyka regulatora PID](Charakterystyka.png)

Powyższy wykres przedstawia charakterystykę skokową systemu regulacji temperatury z zadaną temperaturą 27.0°C. Widoczne jest działanie regulatora PID, który skutecznie doprowadza temperaturę do wartości zadanej z minimalnym uchybem regulacji. Po ustabilizowaniu wykresu błąd wynosił około 3-4%.

## 🧮 Analityczna weryfikacja nastaw (Estymacja)

W celu weryfikacji i dostrojenia nastaw regulatora, posłużono się analizą charakterystyki skokowej układu (widocznej na wykresie). Wykorzystano zmodyfikowane podejście oparte na metodzie Zieglera-Nicholsa, estymując parametry dynamiczne obiektu na podstawie obserwowanych oscylacji.

### 1. Identyfikacja parametrów z wykresu

Mimo że układ wykazuje stabilność (oscylacje gasnące), widoczna cykliczność pozwala na wyznaczenie naturalnego okresu drgań układu, co jest kluczowe dla doboru czasu zdwojenia (Ti) i wyprzedzenia (Td).

| Parametr                   | Opis                                                    | Wartość Szacowana |
| -------------------------- | ------------------------------------------------------- | ----------------- |
| **Tosc** (Okres oscylacji) | Czas pomiędzy kolejnymi szczytami temperatury (t₂ - t₁) | 600s              |
| **Charakter**              | Oscylacje gasnące (układ niedotłumiony)                 | -                 |

**Obliczenie okresu z wykresu:**

- Szczyt 1 (maksimum przeregulowania): t₁ ≈ 400s
- Szczyt 2 (kolejne lokalne maksimum): t₂ ≈ 1000s
- **Tosc = t₂ - t₁ = 1000s - 400s = 600s**

### 2. Dobór nastaw na podstawie estymacji

Przyjmując wyznaczony okres Tosc jako przybliżenie okresu krytycznego Tu, zastosowano reguły strojenia dla regulatora PID:

#### Część całkująca (Ti)

Według reguł inżynierskich, czas zdwojenia powinien być zbliżony do połowy okresu naturalnych oscylacji, aby skutecznie likwidować uchyb bez wprowadzania niestabilności.

```
Ti ≈ 0.5 · Tosc = 300s
```

Dla Kp = 400, wyliczone Ki:

```
Ki = (Kp · Ts) / Ti = (400 · 1) / 300 ≈ 1.33
```

> **Uwaga:** W projekcie finalnie wzmocniono akcję całkującą do Ki = 10 ze względu na dużą bezwładność termiczną grzałki.

#### Część różniczkująca (Td)

Teoretycznie:

```
Td ≈ 0.125 · Tosc = 75s
Kd = (Kp · Td) / Ts = 30000
```

> **Uwaga:** W implementacji cyfrowej tak wysokie Kd powodowało wzmocnienie szumów pomiarowych, dlatego parametr ten został ograniczony eksperymentalnie do wartości 50.

### 📝 Wnioski

Analiza wykresu potwierdza poprawność przyjętego rzędu wielkości nastaw. Układ zachowuje się stabilnie (amplituda oscylacji maleje w czasie), a okres oscylacji wynoszący około 10 minut (600s) świadczy o dużej stałej czasowej obiektu cieplnego. Przyjęte nastawy (Kp = 400, Ki = 10, Kd = 50) zapewniają kompromis między szybkością dochodzenia do temperatury zadanej a stabilnością regulacji.
