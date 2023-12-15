#importer de biblioteker programmet har brug for
import random
import arcade
import math

#sæt bredden og højden af vinduet
BREDDE = 1000
HØJDE = 800



#definer klassen "Sol"
class Sol:
    #definer init-funktionen der kører når objektet bliver skabt
    def __init__(self, fast_punkt, retningsvektor, farve,navn):
        self.fast_punkt = fast_punkt
        self.retningsvektor = retningsvektor
        #start punktet ved et defineret punkt
        self.punkt = self.fast_punkt
        self.farve = farve
        self.navn = navn

    #definer opdaterfunktionen der kører for hver tick af delta_tid
    def opdater(self, delta_tid):
        x, y = self.punkt
        velocitet_x, velocitet_y = self.retningsvektor
        #tilføj retningsvektoren til x og y koordinaten hvert tick
        x += velocitet_x * delta_tid
        y += velocitet_y * delta_tid
        #definer punktet så den kan lave et nyt punkt næste tick
        self.punkt = (x, y)
        #nulstil solens position, hvis den går ud over skærmens bredde og højde
        if x >= BREDDE:
            self.punkt = (-60, y)
            Vindue.ny_stjerne(self)
        if y <= 0:
            self.punkt = (x, HØJDE)
            Vindue.ny_stjerne(self)
    def tegn(self):
        #tegn punktet ved det punkt der blev udregnet i opdaterfunktionen
        x, y = self.punkt
        arcade.draw_circle_filled(x, y, 50, self.farve)
        #tegn tekst der er placeret nedenunder solen
        text_x = x - 20
        text_y = y - 20
        arcade.draw_text(self.navn, text_x, text_y, arcade.color.BLACK, 12)
        arcade.draw_text(self.navn, text_x, text_y, arcade.color.WHITE, 10)


#lav klassen planet, der bruges til at tegne alle planeterne.
class Planet:
    def __init__(self, centrum, radius, vinkelhastighed, vinkel, farve, elipse_bredde, navn, størrelse ):
        self.centrum = centrum
        self.radius = radius
        self.vinkelhastighed = vinkelhastighed
        self.vinkel = vinkel
        #Udregn hvor det første punkt skal placeres ud fra formlen: x = centrum_x + r * cos(v), y = centrum_y + r * sin(v)
        self.punkt = centrum[0] + self.radius * math.cos(self.vinkel), centrum[1] + self.radius * math.sin(self.vinkel)
        self.farve = farve
        self.elipse_bredde = elipse_bredde
        self.navn = navn
        self.størrelse = størrelse


    def opdater(self, delta_tid):
        #ændre vinkelen ud fra vinkelhastigheden og tiden.
        self.vinkel += self.vinkelhastighed * delta_tid
        #tegn punktet med samme formel som før, men ganger her en ellipsebredde på x-koordinaten for at gørre det til en ellipsebane.
        self.punkt = self.centrum[0] + self.elipse_bredde * self.radius * math.cos(self.vinkel), self.centrum[1] + self.radius * math.sin(
            self.vinkel)

    def tegn(self):
        x, y = self.punkt
        #tegn selve planeten med en defineret størrelse og farve
        arcade.draw_circle_filled(x, y, self.størrelse, self.farve)
        #tegn teksten for navnet af planeten.
        text_x = x - 20
        text_y = y -40
        arcade.draw_text(self.navn,text_x,text_y, arcade.color.WHITE, 10)


#lav klassen vindue, der skaber selve vinduet til programmet og grafikken.
class Vindue(arcade.Window):
    def __init__(self, bredde, højde, title):
        super().__init__(bredde, højde, title)
        arcade.set_background_color(arcade.csscolor.BLACK)

    def setup(self):
        #definer alle planeterne og solens variabler
        self.sol = Sol((50, 400), (100, 0), arcade.csscolor.YELLOW, "Solen")
        self.jord = Planet(self.sol.punkt, 130, 1, 0, arcade.csscolor.GREEN, 1.1,"Jorden", 12)
        self.måne = Planet(self.jord.centrum, 23, 13.51, 0, arcade.csscolor.GREY, 1.1, "Månen",6)
        self.merkur = Planet(self.sol.punkt,100,4.14,0,arcade.color.DARK_KHAKI,1.3, "Merkur", 12)
        self.venus = Planet(self.sol.punkt, 150, 1.63,0,arcade.color.ORANGE, 1.1, "Venus", 5)
        self.mars = Planet(self.sol.punkt, 200,0.531,0,arcade.color.BURNT_ORANGE,1.1,"Mars", 6.7)
        self.saturn_ring1 = Planet(self.sol.punkt, 240, 0.033, 50, arcade.color.WHITE, 1.1, "", 20)
        self.saturn_ring2 = Planet(self.sol.punkt, 240, 0.033, 50, arcade.color.BLACK, 1.1, "", 17)
        self.saturn = Planet(self.sol.punkt, 240,0.033, 50, arcade.color.WHITE_SMOKE,1.1,"Saturn", 15)
        self.jupiter = Planet(self.sol.punkt, 280,0.084, 0 ,arcade.color.KHAKI, 1.1, "Jupiter", 22 )
        self.uranus = Planet(self.sol.punkt, 340,0.0119,90, arcade.color.LIGHT_BLUE, 1.1, "Uranus", 17 )
        self.neptun = Planet(self.sol.punkt, 400, 0.00606, 180, arcade.color.DARK_BLUE, 1.1, "Neptun", 16)
        self.pluto = Planet(self.sol.punkt, 450,0.00403,230, arcade.color.GRAY, 1.1, "Pluto", 2.4)
        #lav en liste til alle objekterne i kuiperbeltet
        self.kuiper = []
        for i in range(150):
            #lav en planet med tilfældig radius fra solen, tilfældig vinkelhastighed, og tilfældig startvinkel
            astroide = Planet(self.sol.punkt, (300-random.randint(0,200)),(random.randrange(1,2)), random.randrange(0,360), arcade.color.GRAY, 1.1,"", random.randrange(1,2))
            #tilføj alle alle objekterne til listen
            self.kuiper.append(astroide)
        #lav en liste til alle stjernerne
        self.stjerner = []
        self.ny_stjerne()
    def ny_stjerne(self):
        self.stjerner = []
        #lav x- og y-koordinater til stjerne på baggrunden.
        for l in range(500):
            x = random.randint(0, BREDDE)
            y = random.randint(0, HØJDE)
            self.stjerne = x, y
            self.stjerner.append(self.stjerne)




    def update(self, delta_tid):
        #sæt centrumet for alle planeterne i forhold til hvad de skal kræse om
        self.jord.centrum = self.sol.punkt
        self.måne.centrum = self.jord.punkt
        self.merkur.centrum = self.sol.punkt
        self.venus.centrum = self.sol.punkt
        self.mars.centrum = self.sol.punkt
        self.jupiter.centrum = self.sol.punkt
        self.saturn_ring1.centrum = self.sol.punkt
        self.saturn_ring2.centrum = self.sol.punkt
        self.saturn.centrum = self.sol.punkt
        self.uranus.centrum = self.sol.punkt
        self.neptun.centrum = self.sol.punkt
        self.pluto.centrum = self.sol.punkt
        #gør centrumet af alle objekterne i kuiperbeltet til solens centrum
        for astroide in self.kuiper:
            astroide.centrum = self.sol.punkt

        #opdater alle planeternes positioner.
        self.sol.opdater(delta_tid)
        self.jord.opdater(delta_tid)
        self.måne.opdater(delta_tid)
        self.merkur.opdater(delta_tid)
        self.venus.opdater(delta_tid)
        self.mars.opdater(delta_tid)
        self.saturn_ring1.opdater(delta_tid)
        self.saturn_ring2.opdater(delta_tid)
        self.saturn.opdater(delta_tid)
        self.jupiter.opdater(delta_tid)
        self.uranus.opdater(delta_tid)
        self.neptun.opdater(delta_tid)
        self.pluto.opdater(delta_tid)
        #opdater alle objekternes position
        for astroide in self.kuiper:
            astroide.opdater(delta_tid)

    def on_draw(self):
        self.clear()
        #tegn alle stjernene
        for i in self.stjerner:
            arcade.draw_circle_filled(i[0], i[1], 2, arcade.color.WHITE)
        #tegn alle planeterne
        self.jord.tegn()
        self.måne.tegn()
        self.merkur.tegn()
        self.sol.tegn()
        self.venus.tegn()
        self.mars.tegn()
        self.saturn_ring1.tegn()
        self.saturn_ring2.tegn()
        self.saturn.tegn()
        self.jupiter.tegn()
        self.uranus.tegn()
        self.neptun.tegn()
        self.pluto.tegn()
        #tegn alle objekterne i kuiperbeltet.
        for astroide in self.kuiper:
            astroide.tegn()

def main():
    #start vinduet
    vindue = Vindue(BREDDE, HØJDE, "Solsystemet")
    vindue.setup()
    arcade.run()


#kald main-funktionen for at starte programmet.
main()




