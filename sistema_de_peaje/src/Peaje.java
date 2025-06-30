import java.util.ArrayList;

public class Peaje {
    private String nombre;
    private ArrayList<Vehiculo> vehiculos;
    private int totalPeaje = 0;

    public Peaje(String nombre) {
        this.nombre = nombre;
        this.vehiculos = new ArrayList<>();
    }

    public void añadirVehiculo(Vehiculo v) {
        vehiculos.add(v);
        totalPeaje += v.getValorPeaje();
    }

    public String reporte() {
        StringBuilder sb = new StringBuilder();
        sb.append("Reporte de ").append(nombre).append("\n");
        for (Vehiculo v : vehiculos) {
            sb.append(v.toString()).append("\n");
        }
        sb.append("Total recaudado: $").append(totalPeaje).append("\n");
        return sb.toString();
    }

    public String getNombre() {
        return nombre;
    }
}
