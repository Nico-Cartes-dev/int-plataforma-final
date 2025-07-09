using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using BuenosAires.Model;
using BuenosAires.Model.Utiles;
using Newtonsoft.Json;
using BuenosAires.BodegaBA.WsAnwoReference;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaReservarAnwo : Form
    {
        public VentanaReservarAnwo()
        {
            InitializeComponent();

            gridEquiposAnwo.Columns.Clear();
            gridEquiposAnwo.AutoGenerateColumns = false;
            gridEquiposAnwo.Columns.Add(new DataGridViewTextBoxColumn
            {
                DataPropertyName = "nroserieanwo",
                Name = "nroserieanwo",
                HeaderText = "Nro Serie"
            });
            gridEquiposAnwo.Columns.Add(new DataGridViewTextBoxColumn
            {
                DataPropertyName = "nomprodanwo",
                Name = "nomprodanwo",
                HeaderText = "Nombre"
            });
            gridEquiposAnwo.Columns.Add(new DataGridViewTextBoxColumn
            {
                DataPropertyName = "precioanwo",
                Name = "precioanwo",
                HeaderText = "Precio"
            });
            gridEquiposAnwo.Columns.Add(new DataGridViewTextBoxColumn
            {
                DataPropertyName = "reservado",
                Name = "reservado",
                HeaderText = "Reservado"
            });
            DataGridViewButtonColumn btnCol = new DataGridViewButtonColumn();
            btnCol.DataPropertyName = "opciones";
            btnCol.Name = "opciones";
            btnCol.HeaderText = "Opciones";
            btnCol.Text = "Reservar";
            btnCol.UseColumnTextForButtonValue = true;
            gridEquiposAnwo.Columns.Add(btnCol);

            gridEquiposAnwo_CellClick(null, null);
        }

        public class RootAnwo
        {
            public List<StockItemAnwo> data { get; set; }
        }


        public class StockItemAnwo
        {
            public string nroserieanwo { get; set; }
            public string nomprodanwo { get; set; }
            public int? precioanwo { get; set; }
            public string reservado { get; set; }
            public string opciones { get; set; }
        }

        private void btnVolver_Click(object sender, EventArgs e)
        {
            new VentanaPrincipal().Show();
            Hide();
        }
        private void gridEquiposAnwo_CellClick(object sender, DataGridViewCellEventArgs e)
        {
            try
            {
                var ws = new WsAnwoClient();

                // Correct the issue by removing the assignment to a variable since the method returns void.
                //var respuesta = await ws.Consultar_productos_disponiblesAsync();

                // Assuming the service call updates the data source internally or another method is used to fetch the data.
                var respuesta = ws.Consultar_productos_disponibles(); // Replace with actual method to retrieve response.


                if (!respuesta.HayErrores)
                {
                    var root = JsonConvert.DeserializeObject<RootAnwo>(respuesta.JsonListaStockAnwo);
                    gridEquiposAnwo.DataSource = root.data;

                    //var equipos = JsonConvert.DeserializeObject<List<StockItemAnwo>>(respuesta.JsonListaStockAnwo);
                    //gridEquiposAnwo.DataSource = equipos;
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

        // evento que ejecuta el metodo de la api "reservar_anwo"
        // cuando se clikea la celda reservar
        private void gridEquiposAnwo_CellContentClick_1(object sender, DataGridViewCellEventArgs e)
        {
            try
            {
                var ws = new WsAnwoClient();
                var respuesta = ws.reservar_equipo_anwo(
                    gridEquiposAnwo.Rows[e.RowIndex].Cells["nroserieanwo"].Value.ToString(),
                    gridEquiposAnwo.Rows[e.RowIndex].Cells["reservado"].Value.ToString().ToUpperInvariant() == "S" ? 'N' : 'S'
                    );

                if (!respuesta.HayErrores)
                {
                    MessageBox.Show(respuesta.Mensaje, "Exito", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    // carga de nuevo la tabla despues de la reserva
                    gridEquiposAnwo_CellClick(null, null);

                }
                else
                {
                    MessageBox.Show(respuesta.Mensaje, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error al reservar el equipo: " + ex.Message, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }
    }
}
