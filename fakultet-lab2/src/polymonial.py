class Polynomial:
    """
    Klasa reprezentująca wielomian.
    Współczynniki są przechowywane w liście coeff, gdzie:
    - pierwszy element to współczynnik przy najwyższej potędze
    - ostatni element to wyraz wolny

    Przykład: 3x^2 + 2x + 1 będzie reprezentowane jako [3, 2, 1]
    """

    def __init__(self, coefficients):
        """
        Inicjalizacja wielomianu z listy współczynników.

        Args:
            coefficients: Lista współczynników, pierwszy element to współczynnik przy najwyższej potędze
        """
        # Kopiujemy listę, aby uniknąć przypadkowych modyfikacji zewnętrznych
        self.coeff = list(coefficients)

        # Usuwamy zbędne zera z lewej strony
        self._remove_leading_zeros()

        # Jeśli lista jest pusta, to ustawiamy wielomian zerowy [0]
        if not self.coeff:
            self.coeff = [0]

    def _remove_leading_zeros(self):
        """Usuwa zbędne zera z lewej strony (przy najwyższych potęgach)."""

        while len(self.coeff) > 1 and self.coeff[0] == 0:
            self.coeff.pop(0)

    def degree(self):
        """Zwraca stopień wielomianu."""

        return len(self.coeff)-1

    def evaluate(self, x):
        """
        Oblicza wartość wielomianu dla danego x za pomocą schematu Hornera.

        Args:
            x: Wartość, dla której obliczamy wielomian

        Returns:
            Wartość wielomianu w punkcie x
        """

        ans = self.coeff[0]

        for i in range(1,len(self.coeff)):

            ans = ans * x + self.coeff[i]

        return ans

    def __str__(self):
        """Zwraca czytelną reprezentację wielomianu jako string."""

        if len(self.coeff) == 1:
            return f"{self.coeff[0]}"

        ans = ""

        for i in range(0, len(self.coeff)):

            power = len(self.coeff) - i - 1
            val = self.coeff[i]

            if val == 0:
                continue

            if val == 1 and power != 0:
                val_str = ""
            elif val == -1 and power != 0:
                val_str = "-"
            else:
                val_str = str(val)


            if power == 1:
                power_str = "x"
            elif power == 0:
                power_str = ""
            else:
                power_str = f"x^{power}"


            if ans == "":
                ans = val_str + power_str
            else:
                if val > 0:
                    ans += " + " + val_str + power_str
                else:
                    ans += " - " + val_str.lstrip("-") + power_str

        return ans

    def __repr__(self):
        """Zwraca reprezentację wielomianu do debugowania."""
        return f"Polynomial({self.coeff})"

    def __eq__(self, other):
        """
        Porównuje dwa wielomiany.

        Args:
            other: Inny wielomian lub liczba do porównania.

        Returns:
            True jeśli wielomiany są równe, False w przeciwnym przypadku.
        """
        if isinstance(other, Polynomial):
            return self.coeff == other.coeff

        elif isinstance(other, (int, float)):
            return len(self.coeff) == 1 and self.coeff[0] == other
        return False

    def __add__(self, other):
        """
        Dodaje dwa wielomiany lub wielomian i liczbę.

        Args:
            other: Inny wielomian lub liczba do dodania

        Returns:
            Nowy wielomian będący sumą
        """

        if isinstance(other, Polynomial):
            if len(self.coeff) >= len(other.coeff):
                larger, smaller = self.coeff.copy(), other.coeff
            else:
                larger, smaller = other.coeff.copy(), self.coeff

            for i in range(1, len(smaller) + 1):
                larger[-i] += smaller[-i]

            return Polynomial(larger)

        if isinstance(other,(int, float)):

            ans = self.coeff.copy()
            ans[-1] += other
            return Polynomial(ans)



    def __radd__(self, other):
        """
        Obsługuje dodawanie z liczbą po lewej stronie.

        Args:
            other: Liczba do dodania po lewej stronie

        Returns:
            Nowy wielomian będący sumą
        """
        return self + other

    def __sub__(self, other):
        """
        Odejmuje wielomian lub liczbę od tego wielomianu.

        Args:
            other: Wielomian lub liczba do odjęcia

        Returns:
            Nowy wielomian będący różnicą
        """

        if isinstance(other, Polynomial):
            if len(self.coeff) >= len(other.coeff):
                larger, smaller = self.coeff.copy(), other.coeff
            else:
                larger, smaller = other.coeff.copy(), self.coeff

            for i in range(1, len(smaller) + 1):
                larger[-i] -= smaller[-i]

            return Polynomial(larger)

        if isinstance(other, (int, float)):
            ans = self.coeff.copy()
            ans[-1] -= other
            return Polynomial(ans)

    def __rsub__(self, other):
        """
        Obsługuje odejmowanie wielomianu od liczby (liczba po lewej stronie).

        Args:
            other: Liczba, od której odejmujemy wielomian

        Returns:
            Nowy wielomian będący różnicą
        """
        ans = [-c for c in self.coeff]
        ans[-1] = other - self.coeff[-1]
        return Polynomial(ans)

    def __mul__(self, other):
        """
        Mnoży wielomian przez inny wielomian lub liczbę.

        Args:
            other: Wielomian lub liczba do pomnożenia

        Returns:
            Nowy wielomian będący iloczynem
        """
        if isinstance(other, Polynomial):
            result = [0] * (len(self.coeff) + len(other.coeff) - 1)
            for i in range(len(self.coeff)):
                for j in range(len(other.coeff)):
                    result[i+j] += self.coeff[i] * other.coeff[j]
            return Polynomial(result)

        if isinstance(other, (int, float)):
            ans = []
            for el in self.coeff:
                ans.append(el * other)
            return Polynomial(ans)



    def __rmul__(self, other):
        """
        Obsługuje mnożenie liczby przez wielomian (liczba po lewej stronie).

        Args:
            other: Liczba do pomnożenia po lewej stronie

        Returns:
            Nowy wielomian będący iloczynem
        """
        return  self * other

p1 = Polynomial([3, 2, 1])
p2 =  Polynomial([2, 3, -1])
p3 = Polynomial([5, 4])
print(5 - p1)
