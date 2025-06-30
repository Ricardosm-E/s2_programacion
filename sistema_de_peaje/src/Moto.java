public class Moto extends Vehiculo {
    private int valorPeaje = 1;

    public Moto(String placa) {
        super(placa);
    }

    @Override
    public int getValorPeaje() {
        return valorPeaje;
    }

    @Override
    public String toString() {
        return "Moto - Placa: " + placa + " - Peaje: $" + valorPeaje;
    }
}
