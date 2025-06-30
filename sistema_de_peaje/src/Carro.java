public class Carro extends Vehiculo {
    private int valorPeaje = 2;

    public Carro(String placa) {
        super(placa);
    }

    @Override
    public int getValorPeaje() {
        return valorPeaje;
    }

    @Override
    public String toString() {
        return "Carro - Placa: " + placa + " - Peaje: $" + valorPeaje;
    }
}
