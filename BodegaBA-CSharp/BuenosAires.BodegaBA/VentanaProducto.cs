using System;
using System.Windows.Forms;
using System.Collections.Generic;
using BuenosAires.Model;
using BuenosAires.Model.Utiles;
using BuenosAires.ServiceProxy;

namespace BuenosAires.BodegaBA
{
    public partial class VentanaProducto : Form
    {
        public VentanaProducto(string cuenta )
        {
            InitializeComponent();
            this.Text = $"Mantenedor de productos - Usuario_ {cuenta}";
            btnBuscar.Click += (sender, e) => Buscar();
            btnNuevo.Click += (sender, e) => Nuevo();
            btnGuardar.Click += (sender, e) => Guardar();
            btnEliminar.Click += (sender, e) => Eliminar();
            btnCargarProductos.Click += (sender, e) => CargarProductos();
            grid.SelectionChanged += (sender, e) => Seleccionar();
            grid.ConfigurarDataGridView(
                  "idprod:ID,"
                + "nomprod:Nombre,"
                + "descprod:Descripcion,"
                + "precio:Precio,"
                + "imagen:Imagen"
                );
            CargarProductos();
            this.CentrarVentana();
        }


        private void Nuevo()
        {
            this.Limpiar(new TextBox[]
            {
                txtIdProd,
                txtNomProd,
                txtDescProd,
                txtPrecio,
                txtImagen

            });
        }

        public bool ValidarCamposNumericos()
        {
            if (txtIdProd.Text != "" && txtIdProd.EsNumero())
            {
                return this.ErrEntero("ID");
            }
            if (txtPrecio.Text != "" && txtIdProd.EsNumero())
            {
                return this.ErrEntero("ID");
            }
            return true;

        }

        private void Seleccionar()
        {
            if (grid.SelectedRows.Count <= 0) return;

            DataGridViewRow row = grid.SelectedRows[0];
            if (row.GetString("idprod") != "0")
            {
                this.AsignarValoresTextBox(row);
            }
            txtNomProd.FocusToEnd();
        }

        private bool Buscar()
        {
            int id = new VentanaBuscarID().MostrarVentanaModal(); // Corrected method name
            if (id == -1) return false;

            var bc = new ScProducto();
            bc.Leer(id);

            if (bc.Producto == null) return this.MensajeError(bc.Mensaje);

            CargarProductos();
            this.AsignarValoresTextBox(bc.Producto);

            grid.SeleccionarId("idprod", txtIdProd.ToInt());
            txtNomProd.FocusToEnd();
            return true;
        }

        private void Guardar()
        {
            if (!ValidarCamposNumericos()) return;

            var prod = new Producto();
            prod.idprod = txtIdProd.ToIntOrDefault();
            prod.nomprod = txtNomProd.Text;
            prod.descprod = txtDescProd.Text;
            prod.precio = txtPrecio.ToInt();
            prod.imagen = txtImagen.Text;

            var bc = new ScProducto();

            if (txtIdProd.Text.Trim() == "")
            {
                bc.Crear(prod);
            }
            else
            {
                bc.Actualizar(prod);
            }

            if(!bc.HayErrores)
            {
                txtIdProd.SetText(bc.Producto.idprod);
                CargarProductos();
                grid.SeleccionarId("idPro", bc.Producto.idprod);
                txtNomProd.FocusToEnd();
            }
            this.MensajeInfo(bc.Mensaje);
        }

        private bool Eliminar()
        {
            var bc = new ScProducto();
            if (txtIdProd.Text.Trim() == "")
            {
                return this.ErrAccionID("ID", "eliminar");
            }
            bc.Eliminar(txtIdProd.ToInt());
            CargarProductos();
            this.MensajeInfo(bc.Mensaje);
            return true;
        }
        

        public void CargarProductos()
        {
            var bc = new ScProducto();
            bc.LeerTodos();
            grid.DataSource = bc.Lista;
            grid.RefrescarYajustar();
            if (bc.HayErrores == true) this.MensajeInfo(bc.Mensaje);
        }

        private void btnNuevo_Click(object sender, EventArgs e)
        {

        }
    }
}
