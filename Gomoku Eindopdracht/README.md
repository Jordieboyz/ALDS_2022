# uitleg voor de must-haves


# 1, works for both
Ik creer een nieuwe root van elke 'move'aanroep. hierdoor hoef ik niet
elke keer een nieuwe tree te maken, maar alleen een soort subset van het geheel en het voorkomt dat
ik per ongeluk te ver terug in de tree ga. Ik exploit maar 1 linie van hchildren en vanuit die chuildren doe ik een random rollout.
Het is dus niet echt een tree, maar een subset van een tree.

# 2, works for both
Door de 'star points' van het 19x19 board te nemen, creer je een territorium om makkelijk aan te kunnen vallen
en verdedigen. ik heb mijn star points zo gekozen dat er een directe rij van 5 stenen kan worden gecreerd. zo maakn ik het mezelf
dus makkelijk omdat ik meteen aanvallend speel.

#3
TODO: constant c exploration value experiment

adj moves, prevent whole board search, set around 800 loops to rollout w matrix of 2

