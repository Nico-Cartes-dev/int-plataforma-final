using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using BuenosAires.BodegaBA;
using BuenosAires.Model.Utiles;
using BuenosAires.ServiceProxy;


namespace BuenosAires.BodegaBA
{
    public partial class VentanaLogin : Form
    {
        public VentanaLogin()
        {
            InitializeComponent();
            this.AcceptButton = btnIngresar;
            this.StartPosition = FormStartPosition.CenterScreen;
        }


        private void btnIngresar_Click(object sender, EventArgs e)
        {
            var sc = new ScAutenticacion();
            sc.Autenticar("Bodeguero", txtCuenta.Text, txtPassword.Text);
            if (sc.Autenticado)
            {
                new VentanaPrincipal(sc.NombreUsuario + "(" + sc.TipoUsuario + ")").Show();
                Hide();
            }
            else
            {
                this.MensajeInfo(sc.Mensaje);
            }
        }
    }
}
