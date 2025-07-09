using System;
using System.Collections;
using System.Collections.Generic;
using System.Data.Entity.Validation;
using System.IO;
using System.Reflection;
using System.Text;
using System.Xml;
using System.Xml.Serialization;

namespace BuenosAires.Model.Utiles
{
    public static class Util
    {
        public static string NombreSistema = "Sistema Buenos Aires";

        public static Type GetStaticType(object obj)
        {
            Type objType = null;

            if (obj.GetType().FullName.Contains("System.Data.Entity.DynamicProxies"))
            {
                objType = Type.GetType(obj.GetType().BaseType.FullName + ", " + obj.GetType().BaseType.Assembly);
            }
            else
            {
                objType = obj.GetType();
            }

            return objType;
        }

        public static object GetStaticObject(object obj)
        {
            var objInstance = Activator.CreateInstance(GetStaticType(obj));
            return objInstance;
        }

        private static string SerializarListaXML(object obj)
        {
            if (obj == null) return "";

            XmlSerializer serializer;
            XmlSerializerNamespaces namespaces = 
                new XmlSerializerNamespaces(new[] { XmlQualifiedName.Empty });

            var sb = new StringBuilder();

            using (var writer = new StringWriter(sb))
            {
                var itemType = obj.GetType().GetGenericArguments()[0];
                var listType = typeof(List<>).MakeGenericType(itemType);
                serializer = new XmlSerializer(listType);
                serializer.Serialize(writer, obj, namespaces);
            }

            return sb.ToString();
        }

        private static string SerializarObjetoPocoXML(object obj)
        {
            Type objType = GetStaticType(obj);
            var serializer = new XmlSerializer(objType);
            
            using (var writer = new StringWriter())
            {
                var newObj = GetStaticObject(obj);
                CopiarPropiedades(obj, newObj);
                serializer.Serialize(writer, newObj);
                string xml = writer.ToString();
                return xml;
            }
        }

        public static string SerializarXML(object obj)
        {
            if (obj == null) return "";
            if (obj is IList) return SerializarListaXML(obj);
            return SerializarObjetoPocoXML(obj);
        }

        public static T DeserializarXML<T>(string xml)
        {
            if (string.IsNullOrEmpty(xml)) return default(T);
            var serializer = new XmlSerializer(typeof(T));
            using (var reader = new StringReader(xml))
            {
                var obj = (T)serializer.Deserialize(reader);
                return obj;
            }
        }

        public static string PonerPuntoFinal(string texto)
        {
            texto = texto.Trim();
            if (texto != "")
            {
                if (!texto.EndsWith("."))
                {
                    return texto + ".";
                }
            }
            return texto;
        }

        public static string MensajeError(string accion, string origen, Exception ex)
        {
            var mensajeError = $"No fue posible {accion}. Comuníquese con el Administrador del Sistema.\n\nOrigen: {origen}\n\n";

            if (ex != null)
            {
                if (ex.Message.Trim() != "")
                {
                    if (mensajeError == "")
                    {
                        mensajeError = PonerPuntoFinal(ex.Message);
                    }
                    else
                    {
                        mensajeError += " " + PonerPuntoFinal(ex.Message);
                    }
                }

                if (ex.InnerException != null)
                {
                    if (mensajeError == "")
                    {
                        mensajeError = PonerPuntoFinal(ex.InnerException.Message);
                    }
                    else
                    {
                        mensajeError += " " + PonerPuntoFinal(ex.InnerException.Message);
                    }

                    if (ex.InnerException.InnerException != null)
                    {
                        if (mensajeError == "")
                        {
                            mensajeError = PonerPuntoFinal(ex.InnerException.InnerException.Message);
                        }
                        else
                        {
                            mensajeError += " " + PonerPuntoFinal(ex.InnerException.InnerException.Message);
                        }
                    }
                }

                if (ex is DbEntityValidationException)
                {
                    StringBuilder errorMessage = new StringBuilder();

                    foreach (var error in ((DbEntityValidationException)ex).EntityValidationErrors)
                    {
                        foreach (var validationError in error.ValidationErrors)
                        {
                            string propertyName = validationError.PropertyName;
                            string errorMessagePart = $"{propertyName}: {validationError.ErrorMessage}";
                            errorMessage.AppendLine(errorMessagePart);
                        }
                    }
                    mensajeError += errorMessage.ToString();
                }
            }

            if (mensajeError == "") mensajeError = "ERROR: Comuníquese con el Administrador del Sistema.";

            return mensajeError;
        }

        public static bool CopiarPropiedades(object objetoOrigen, object objetoDestino)
        {
            if (objetoOrigen == null || objetoDestino == null) return false;

            // Copiar propiedades
            var tipo = objetoOrigen.GetType();
            var propiedades = tipo.GetProperties();

            foreach (var propiedad in propiedades)
            {
                try
                {
                    var propInfo = objetoDestino.GetType().GetProperty(propiedad.Name);
                    if (propInfo != null && propInfo.CanWrite)
                    {
                        var valorOrigen = propiedad.GetValue(objetoOrigen, null);

                        if (valorOrigen != null && typeof(System.Collections.IEnumerable).IsAssignableFrom(valorOrigen.GetType()) && !valorOrigen.GetType().Equals(typeof(string)))
                        {
                            var tipoElemento = propInfo.PropertyType.GetGenericArguments()[0];
                            var listaDestino = Activator.CreateInstance(typeof(List<>).MakeGenericType(tipoElemento)) as System.Collections.IList;

                            foreach (var item in (System.Collections.IEnumerable)valorOrigen)
                            {
                                var itemDestino = Activator.CreateInstance(tipoElemento);
                                CopiarPropiedades(item, itemDestino);
                                listaDestino.Add(itemDestino);
                            }

                            propInfo.SetValue(objetoDestino, listaDestino);
                        }
                        else
                        {
                            propInfo.SetValue(objetoDestino, valorOrigen);
                        }
                    }
                }
                catch
                {
                    // Ignorar errores
                }
            }

            // Copiar campos
            var campos = tipo.GetFields();

            foreach (var campo in campos)
            {
                try
                {
                    var fieldInfo = objetoDestino.GetType().GetField(campo.Name);
                    if (fieldInfo != null)
                    {
                        var valorOrigen = campo.GetValue(objetoOrigen);

                        if (valorOrigen != null && typeof(System.Collections.IEnumerable).IsAssignableFrom(valorOrigen.GetType()) && !valorOrigen.GetType().Equals(typeof(string)))
                        {
                            var tipoElemento = fieldInfo.FieldType.GetGenericArguments()[0];
                            var listaDestino = Activator.CreateInstance(typeof(List<>).MakeGenericType(tipoElemento)) as System.Collections.IList;

                            foreach (var item in (System.Collections.IEnumerable)valorOrigen)
                            {
                                var itemDestino = Activator.CreateInstance(tipoElemento);
                                CopiarPropiedades(item, itemDestino);
                                listaDestino.Add(itemDestino);
                            }

                            fieldInfo.SetValue(objetoDestino, listaDestino);
                        }
                        else
                        {
                            fieldInfo.SetValue(objetoDestino, valorOrigen);
                        }
                    }
                }
                catch
                {
                    // Ignorar errores
                }
            }

            return true;
        }

    }
}
