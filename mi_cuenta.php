<!DOCTYPE html>
<html>
<head>

    <?php include("includes/head.php") ?>

</head>
<body>

    <!-- Header -->
    <?php include ("includes/header.php")?>

    <div class="container">
        <div class="row">
            <div class="col-md-12">
                <ol class="breadcrumb">
                    <li><a href="#">Inicio</a></li>
                    <li class="active">Mi Cuenta</li>
                </ol>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="row">

            <div class="col-md-offset-1 col-md-10 col-md-offset-1">

                <div class="page-header margin-0">
                  <h1 class="margin-0">Mi cuenta <small>Configuracion general</small></h1>
                </div>

                <br>

                <table class="table table-striped">
                  <tbody>

                    <tr>
                      <td><p><b>Nombre</b></p></td>
                      <td><p>Juan Perez</p></td>
                      <td><p><a href="#">Editar</a></p></td>
                    </tr>

                    <tr>
                      <td><p><b>Nombre de usuario</b></p></td>
                      <td><p>JuanPerez01</p></td>
                      <td><p><a href="#">Editar</a></p></td>
                    </tr>

                    <tr>
                      <td><p><b>Correo</b></p></td>
                      <td><p>juan_perez@gmail.com</p></td>
                      <td><p><a href="#">Editar</a></p></td>
                    </tr>

                    <tr>
                      <td><p><b>Contraseña</b></p></td>
                      <td><p>Ultima actualizacion - 05-02-2017</p></td>
                      <td><p><a href="#">Editar</a></p></td>
                    </tr>

                    <tr>
                      <td><p><b>Descripcion de usuario</b></p></td>
                      <td><p>Aqui va una breve descripcion que se muestra cuando entras a ver los productos del usuario...</p></td>
                      <td><p><a href="#">Editar</a></p></td>
                    </tr>

                    <tr>
                      <td><p><b>Tipo de usuario</b></p></td>
                      <td><p>Gratis - Premium</p></td>
                      <td><p><a href="#">Editar</a></p></td>
                    </tr>

                    <tr>
                      <td><p><b>Eliminar cuenta</b></p></td>
                      <td><p>Si eliminas tu cuenta se eliminaran tus productos y no los podras recuperar.</p></td>
                      <td><p><a href="#">Eliminar</a></p></td>
                    </tr>

                  </tbody>
                </table>

            </div>
        </div>
    </div>

    <!-- Footer -->
    <?php include ("includes/footer.php")?>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="bootstrap/js/bootstrap.js"></script>

</body>
</html>
