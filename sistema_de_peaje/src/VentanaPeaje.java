import javax.swing.*;
import java.awt.*;
import java.awt.event.*;

public class VentanaPeaje extends JFrame {
    private Peaje[] casetas;
    private JComboBox<String> comboCasetas, comboTipo;
    private JTextField txtPlaca, txtEjes;
    private JTextArea areaSalida;
    private JButton btnRegistrar, btnMostrar;

    public VentanaPeaje() {
        setTitle("Sistema de Peaje");
        setSize(650, 550);
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        // Fondo con imagen
        FondoPanel fondo = new FondoPanel("/peaje.jpg"); // ← Usa "/" si está en carpeta resources o misma ruta
        fondo.setLayout(new FlowLayout());

        
        casetas = new Peaje[] {
                new Peaje("Peaje A"), new Peaje("Peaje B"),
                new Peaje("Peaje C"), new Peaje("Peaje D")
        };

        comboCasetas = new JComboBox<>(new String[] { "Peaje A", "Peaje B", "Peaje C", "Peaje D" });
        comboTipo = new JComboBox<>(new String[] { "Carro", "Moto", "Camión" });
        txtPlaca = new JTextField(10);
        txtEjes = new JTextField(5);
        areaSalida = new JTextArea(18, 50);
        areaSalida.setEditable(false);

        JScrollPane scroll = new JScrollPane(areaSalida);

        btnRegistrar = new JButton("Registrar Vehículo");
        btnMostrar = new JButton("Mostrar Reporte Caseta");

        fondo.add(new JLabel("Caseta:"));
        fondo.add(comboCasetas);
        fondo.add(new JLabel("Tipo Vehículo:"));
        fondo.add(comboTipo);
        fondo.add(new JLabel("Placa:"));
        fondo.add(txtPlaca);
        fondo.add(new JLabel("Ejes (si es camión):"));
        fondo.add(txtEjes);
        fondo.add(btnRegistrar);
        fondo.add(btnMostrar);
        fondo.add(scroll);

        setContentPane(fondo);
        setVisible(true);

        btnRegistrar.addActionListener(e -> registrarVehiculo());
        btnMostrar.addActionListener(e -> mostrarReporte());
    }

    private void registrarVehiculo() {
        String placa = txtPlaca.getText().trim();
        String tipo = (String) comboTipo.getSelectedItem();
        int caseta = comboCasetas.getSelectedIndex();

        if (placa.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Ingrese la placa.");
            return;
        }

        try {
            Vehiculo v;
            switch (tipo) {
                case "Carro": v = new Carro(placa); break;
                case "Moto": v = new Moto(placa); break;
                case "Camión":
                    int ejes = Integer.parseInt(txtEjes.getText());
                    v = new Camion(placa, ejes);
                    break;
                default: throw new Exception("Tipo inválido.");
            }
            casetas[caseta].añadirVehiculo(v);
            areaSalida.setText("Vehículo registrado en " + casetas[caseta].getNombre());
            txtPlaca.setText("");
            txtEjes.setText("");
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Error: " + ex.getMessage());
        }
    }

    private void mostrarReporte() {
        int index = comboCasetas.getSelectedIndex();
        areaSalida.setText(casetas[index].reporte());
    }
}
