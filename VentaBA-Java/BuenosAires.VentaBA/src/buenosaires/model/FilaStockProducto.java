/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package buenosaires.model;

/**
 *
 * @author CETECOM
 */

public class FilaStockProducto {
    private int idstock;
    private String nomprod;
    private int cantidad;
    private String estado;
    private String imagen;

    public String getImagen() {
        return imagen;
    }

    public void setImagen(String imagen) {
        this.imagen = imagen;
    }

    // Constructor vacío
    public FilaStockProducto() {
    }

    // Constructor con todos los campos
    public FilaStockProducto(int idstock, String nomprod, int cantidad, String estado, String imagen) {
        this.idstock = idstock;
        this.nomprod = nomprod;
        this.cantidad = cantidad;
        this.estado = estado;
        this.imagen = imagen;
    }

    // Getters y setters
    public int getIdstock() {
        return idstock;
    }

    public void setIdstock(int idstock) {
        this.idstock = idstock;
    }

    public String getNomprod() {
        return nomprod;
    }

    public void setNomprod(String nomprod) {
        this.nomprod = nomprod;
    }

    public int getCantidad() {
        return cantidad;
    }

    public void setCantidad(int cantidad) {
        this.cantidad = cantidad;
    }

    public String getEstado() {
        return estado;
    }

    public void setEstado(String estado) {
        this.estado = estado;
    }

    // toString() para mostrar fácilmente los datos
    @Override
    public String toString() {
        return "FilaStockProducto{" +
                "idstock=" + idstock +
                ", nomprod='" + nomprod + '\'' +
                ", cantidad=" + cantidad +
                ", estado='" + estado + '\'' +
                '}';
    }
}
