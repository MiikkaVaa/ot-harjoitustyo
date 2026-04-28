# Ohjelmistotekniikka | Harjoitustyö | Megazone Ranked-järjestelmä


### Dokumentaatio

- [Vaatimuusmäärittely](dokumentaatio/vaatimusmaarittely.md)
- [Työaikakirjanpito](dokumentaatio/tuntikirjanpito.md)
- [Arkkitehtuurikuvaus](dokumentaatio/arkkitehtuuri.md)
- [Changelog](dokumentaatio/changelog.md)

### Releases

- [Viikko6 Release](https://github.com/MiikkaVaa/ot-harjoitustyo/releases/tag/Viikko6)

- [Viikko5 Release](https://github.com/MiikkaVaa/ot-harjoitustyo/releases/tag/viikko5)

### Asennus

1. Asenna riippuvuudet:
    ```bash
    poetry install

2. Alusta tietokanta ensimmäisellä kerralla:
    ```bash
    poetry run invoke build

3. Käynnistä sovellus:
    ```bash
    poetry run invoke start

### Muita toimintoja

- Testaus:
  
      poetry run invoke test

- Testikattavuus:
  
      poetry run invoke coverage-report


- Pylint:

      poetry run invoke lint
