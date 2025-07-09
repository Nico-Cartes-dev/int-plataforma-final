using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using BuenosAires.BodegaBA.WsGuiaDespacho;
using Newtonsoft.Json;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaGuiasDespacho : Form
    {
        public VentanaGuiasDespacho()
        {
            InitializeComponent();
            this.Load += VentanaGuiasDespacho_Load;
            dataGridViewGuias.CellContentClick += dataGridViewGuias_CellContentClick;
        }

        public class GuiaItem
        {
            public int    nrogd    { get; set; }
            public int    nrofac   { get; set; }
            public int    idprod   { get; set; }
            public string estadogd { get; set; }
            public string nomprod  { get; set; }
            public string rutcli   { get; set; }
        }

        private void VentanaGuiasDespacho_Load(object sender, EventArgs e)
        {
            CargarGuias();
        }

        private void dataGridViewGuias_CellContentClick(object sender, DataGridViewCellEventArgs e)
        {
            if (e.RowIndex < 0) return;
            var colName = dataGridViewGuias.Columns[e.ColumnIndex].Name;
            var item    = (GuiaItem)dataGridViewGuias.Rows[e.RowIndex].DataBoundItem;

            var ws = new WsGuiaDespachoClient();
            if (colName == "colDespachado")
            {
                ws.ActualizarEstadoGuiaDespacho(item.nrogd, "Despachado");
                CargarGuias();
            }
            else if (colName == "colEntregado")
            {
                ws.ActualizarEstadoGuiaDespacho(item.nrogd, "Entregado");
                CargarGuias();
            }
            else if (colName == "colImprimir")
            {
                // TODO: implementar impresión según tus requerimientos
                MessageBox.Show($"Imprimiendo guía {item.nrogd}", "Imprimir",
                                MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private void CargarGuias()
        {
            try
            {
                var ws         = new WsGuiaDespachoClient();
                var respuesta  = ws.ConsultarGuiasDespacho();
                if (!respuesta.HayErrores)
                {
                    var guias = JsonConvert.DeserializeObject<List<GuiaItem>>(respuesta.JsonStockProducto);
                    dataGridViewGuias.DataSource = guias;

                    // Ajusta encabezados
                    dataGridViewGuias.Columns["nrogd"].HeaderText    = "N° Guía";
                    dataGridViewGuias.Columns["nrofac"].HeaderText   = "N° Factura";
                    dataGridViewGuias.Columns["idprod"].HeaderText   = "ID Producto";
                    dataGridViewGuias.Columns["estadogd"].HeaderText = "Estado";
                    dataGridViewGuias.Columns["nomprod"].HeaderText  = "Producto";
                    dataGridViewGuias.Columns["rutcli"].HeaderText   = "RUT Cliente";

                    // Columnas llenan el ancho
                    dataGridViewGuias.AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.Fill;

                    // Agrega columnas de botones al final solo una vez
                    if (!dataGridViewGuias.Columns.Contains("colDespachado"))
                    {
                        var btnDesp     = new DataGridViewButtonColumn { Name = "colDespachado",    Text = "Despachado", UseColumnTextForButtonValue = true, HeaderText = "Despachado" };
                        var btnEntreg   = new DataGridViewButtonColumn { Name = "colEntregado",    Text = "Entregado",  UseColumnTextForButtonValue = true, HeaderText = "Entregado" };
                        var btnImprimir = new DataGridViewButtonColumn { Name = "colImprimir",     Text = "Imprimir",   UseColumnTextForButtonValue = true, HeaderText = "Imprimir" };
                        dataGridViewGuias.Columns.Add(btnDesp);
                        dataGridViewGuias.Columns.Add(btnImprimir);
                        dataGridViewGuias.Columns.Add(btnEntreg);
                    }
                }
                else
                {
                    MessageBox.Show(respuesta.Mensaje, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error al consultar el servicio: " + ex.Message, "Error",
                                MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            // Volver al menú principal
            new VentanaPrincipal().Show();
            Hide();
        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }
    }
}
