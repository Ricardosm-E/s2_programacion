
public class Main {

    public static void main(String[] args) {

        CalculadoraFactorial calculadora = new CalculadoraFactorial();

        System.out.println("Cálculo del factorial del 1 al 13 :");

        for (int i = 1; i <= 13; i++) {
            long resultado = calculadora.factorial(i);
            System.out.println("El factorial de " + i + " es: " + resultado);
        }
    }
}
