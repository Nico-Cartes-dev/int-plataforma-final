using System;
using System.Collections.Generic;
using System.Collections.Specialized;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using BuenosAires.Model;
using BuenosAires.Model.Utiles;


namespace BuenosAires.DataLayer
{
    public class DcProducto
    {
        public string Accion = "";
        public string Mensaje = "";
        public bool HayErrores = false;
        public Producto Producto = null;
        public List<Producto> Lista = null;


        public DcProducto()
        {
            Inicializar("");
        }

        public void Inicializar(string accion)
        {
            this.Accion = accion;
            this.Mensaje = "";
            this.HayErrores = false;
            this.Producto = null;
            this.Lista = null;
        }

        public int ObtenerSiguienteId()
        {
            Inicializar("obtener un siguiente ID");
            try
            {
                using (var bd = new base_datosEntities())
                {
                    int siguienteID = 1;
                    if (bd.Producto.Count() > 0) siguienteID = bd.Producto.Max(p => p.idprod) + 1;
                    this.Mensaje = "Se ha logrado crear el nuevo id ";
                    return siguienteID;
                }
            }
            catch (Exception ex)
            {
                this.HayErrores = true;
                this.Mensaje = Util.MensajeError(this.Accion, "DcProducto.ObtenerSiguienteId", ex);
                return -1;
            }

        }

        public void Crear(Producto producto)
        {
            this.Inicializar($"crear el producto '{producto.nomprod}'");
            try
            {
                using (var bd = new base_datosEntities())
                {
                    int siguienteID = this.ObtenerSiguienteId();
                    if (this.HayErrores) return;
                    producto.idprod = siguienteID;
                    bd.Producto.Add(producto);
                    bd.SaveChanges();
                    this.Producto = producto;
                    this.Mensaje = $"El producto '{producto.nomprod}' fue creado correctamente";
                }
            }
            catch (Exception ex)
            {
                this.HayErrores = true;
                this.Mensaje = Util.MensajeError(this.Accion, "DcProducto.Crear", ex);
            }
        }
        public void LeerTodos()
        {
            try
            {
                using (var bd = new base_datosEntities())
                {
                    this.Lista = bd.Producto.ToList();
                    if (this.Lista.Count == 0) this.Mensaje = "La lista de pdctos se encuentra vacía.";
                }
            }
            catch (Exception ex)
            {
                this.HayErrores = true;
                this.Mensaje = Util.MensajeError(this.Accion, "DcProducto.LeerTodos", ex);

            }

        }

        public void Leer(int idprod)
        {
            this.Inicializar($"obtener el producto con el ID '{idprod}'");
            try
            {
                using(var bd = new base_datosEntities())
                {
                    this.Producto = bd.Producto.FirstOrDefault(r => r.idprod == idprod);
                    if (this.Producto == null) this.Mensaje = $"No fue posible {this.Accion} pues no existe en la base de datos";
                }
            }
            catch (Exception ex)
            {
                this.HayErrores = true;
                this.Mensaje = Util.MensajeError(this.Accion, "DcProducto.Leer", ex);

            }
        }

        public void Actualizar(Producto producto)
        {
            this.Inicializar($"Actualizar el producto '{producto.nomprod}'");
            try
            {
                using (var bd = new base_datosEntities())
                {
                    var encontrado = bd.Producto.FirstOrDefault(p => p.idprod == producto.idprod);
                    if (encontrado == null)
                    {
                        this.Mensaje = $"No fue posible {this.Accion} pues no existe en la base de datos";
                    }
                    else
                    {
                        Util.CopiarPropiedades(producto, encontrado);
                        bd.SaveChanges();
                        this.Producto = new Producto();
                        Util.CopiarPropiedades(producto, this.Producto);
                        this.Mensaje = $"El producto {producto.nomprod} fue actualizado correctamente!";
                    }
                }
            }
            catch (Exception ex)
            {
                this.HayErrores = true;
                this.Mensaje = Util.MensajeError(this.Accion, "DcProducto.Actualizar", ex);

            }

        }
        public void Eliminar(int idprod)
        {
            this.Inicializar($"Eliminar el producto con el ID '{idprod}'");
            try
            {
                using (var bd = new base_datosEntities())
                {
                    var encontrado = bd.Producto.FirstOrDefault(p => p.idprod == idprod);
                    if (encontrado == null)
                    {
                        this.Mensaje = $"No fue posible {this.Accion} pues no existe en la base de datos";
                    }
                    else
                    {
                        bd.Producto.Remove(encontrado);
                        bd.SaveChanges();
                        this.Mensaje = $"El producto {encontrado.nomprod} fue eliminado con éxito";
                    }
                }
            }
            catch (Exception ex)
            {
                this.HayErrores = true;
                this.Mensaje = Util.MensajeError(this.Accion, "DcProducto.Eliminar", ex);

            }
        }
    }
}