using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Newtonsoft.Json;
using BuenosAires.BodegaBA.WsStockproductoreference;
using BuenosAires.Model;

namespace BuenosAires.BodegaBA
{
    public partial class ConsultarBodega : Form
    {
        public ConsultarBodega()
        {
            InitializeComponent();
            this.Load += ConsultarBodega_Load;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            new VentanaPrincipal().Show();
            Hide();
        }

        private void label2_Click(object sender, EventArgs e)
        {
        }

        public class StockItem
        {
            public int idstock { get; set; }
            public string nomprod { get; set; }
            public int? cantidad { get; set; }
            public string estado { get; set; }
        }

        private void dataGridView1_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            try
            {
                var ws = new WsStockProductoClient();
                var respuesta = ws.ObtenerEquiposEnBodega();
                if (!respuesta.HayErrores)
                {
                    var equipos = JsonConvert.DeserializeObject<List<StockItem>>(respuesta.JsonStockProducto);
                    dataGridView1.DataSource = equipos;

                    // ——————————————————————————————
                    // Estas dos líneas hacen que el grid:
                    // 1) Rellene todo el formulario (Dock = Fill)
                    // 2) Ajuste las columnas al ancho disponible
                    dataGridView1.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
                    // ——————————————————————————————
                }
                else
                {
                    MessageBox.Show(respuesta.Mensaje, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error al consultar el servicio: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void ConsultarBodega_Load(object sender, EventArgs e)
        {
            try
            {
                var ws = new WsStockProductoClient();
                var respuesta = ws.ObtenerEquiposEnBodega();
                if (!respuesta.HayErrores)
                {
                    var equipos = JsonConvert.DeserializeObject<List<StockItem>>(respuesta.JsonStockProducto);
                    dataGridView1.DataSource = equipos;

                    // ——————————————————————————————
                    // Aquí también añadimos Dock y AutoSizeColumnsMode
                    dataGridView1.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;
                    // ——————————————————————————————
                }
                else
                {
                    MessageBox.Show(respuesta.Mensaje, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error al consultar el servicio: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
