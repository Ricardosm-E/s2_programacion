public class Camion extends Vehiculo {
    private int numeroEjes;

    public Camion(String placa, int numeroEjes) {
        super(placa);
        this.numeroEjes = numeroEjes;
    }

    @Override
    public int getValorPeaje() {
        // Mínimo $2. Si tiene más de 2 ejes, cada eje adicional suma $1
        return Math.max(2, numeroEjes);
    }

    @Override
    public String toString() {
        return "Camión - Placa: " + placa + " - Ejes: " + numeroEjes + " - Peaje: $" + getValorPeaje();
    }
}
