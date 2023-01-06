# MLEnergiePentruViitor
Proiectul pentru concursul Energie Pentru Viitor, organizat de E.ON in anul 2021.

Tehnologii folosite: Tensorflow

## Descrierea proiectului
Proiectul folosește algoritmi de inteligență artificială pentru a prezice valorile medii date de „panourile solare” pentru zilele următoare.
Programul prelevă în fiecare oră 600 de valori de la senzorii de intensitate luminoasă, pe care le trimite apoi la seria de neuroni care se antrenează cu aceste date plus cele de la prognoza meteo. Acesta învață în ce zile valorile care simulează curentul electric sunt mai ridicate și când scad, în funcție de vreme.

![imagine 1](https://github.com/Minutzu321/MLEnergiePentruViitor/blob/main/imagini/Energie%20pentru%20viitor%20(1).png?raw=true)

## Descrierea senzorilor
Am făcut un circuit simplu cu un microcontroller (raspberry pi), un fotorezistor (care simulează panoul solar), un rezistor simplu și un condensator. Condensatorul este încărcat 2 secunde de unul dintre pinii microcontrolerului, după care este lăsat să se descarce, fotorezistorul opunând rezistență în funcție de intensitatea luminoasă. Microcontrolerul măsoară apoi cât îi ia condensatorului să se descarce și așa interpretează puterea „panourilor”. 
Proiectul are 3 astfel de senzori

![imagine 2](https://github.com/Minutzu321/MLEnergiePentruViitor/blob/main/imagini/Energie%20pentru%20viitor%20(2).png?raw=true)

![imagine 3](https://github.com/Minutzu321/MLEnergiePentruViitor/blob/main/imagini/Energie%20pentru%20viitor%20(3).png?raw=true)

![imagine 4](https://github.com/Minutzu321/MLEnergiePentruViitor/blob/main/imagini/Energie%20pentru%20viitor%20(4).png?raw=true)

## Infrastructura proiectului
Clădirile au fost printate cu ajutorul imprimantei 3d a echipei de robotică. Design-ul îmi aparține complet.
În proiect sunt două microcontrolere: unul care ia datele de la senzori și care ține serverul de informații deschis iar celălalt care le procesează, conectându-se la server și cerând informațiile.
Acest proces se execută odată pe oră, întrucât baza de date de la care luăm datele meteo se actualizează în fiecare oră.

![imagine 5](https://github.com/Minutzu321/MLEnergiePentruViitor/blob/main/imagini/Energie%20pentru%20viitor%20(5).png?raw=true)
![imagine 6](https://github.com/Minutzu321/MLEnergiePentruViitor/blob/main/imagini/Energie%20pentru%20viitor%20(6).png?raw=true)
![imagine 7](https://github.com/Minutzu321/MLEnergiePentruViitor/blob/main/imagini/Energie%20pentru%20viitor%20(7).png?raw=true)
![imagine 8](https://github.com/Minutzu321/MLEnergiePentruViitor/blob/main/imagini/Energie%20pentru%20viitor%20(8).png?raw=true)
## Concluzia
După ce antrenăm modelul, îl punem să facă un grafic cu „pierderea” (termen care face referire la eroarea dintre prezicerile algoritmului și valorile bune). Această pierdere este de două tipuri:
pierdere la antrenament care simbolizează eroarea cu datele cu care a fost antrenat algoritmul
pierderea la validare care simbolizează eroarea cu datele pe care algoritmul nu le-a văzut niciodată
![imagine 9](https://github.com/Minutzu321/MLEnergiePentruViitor/blob/main/pierdere09052021.png?raw=true)
