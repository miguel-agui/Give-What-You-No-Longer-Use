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
            <div class="col-md-offset-4 col-md-4 col-md-offset-4 col-sm-offset-3 col-sm-6 col-sm-offset-3">
                <div class="panel-blue">

                    <form action="" method="post">
                        <div class="form-group">
                            <label>Nombre</label>
                            <input type="email" name="text" class="form-control" placeholder="Nombre completo" required>
                        </div>
                        <div class="form-group">
                            <label>Email</label>
                            <input type="email" name="email" class="form-control" placeholder="ej@mail.com" required>
                        </div>
                        <div class="form-group">
                            <label>Contraseña</label>
                            <input type="password" name="pass" class="form-control" placeholder="Password" required>
                        </div>
                        <div class="checkbox">
                            <label>
                                <input type="checkbox" required> Acepto los <a href="#">Terminos de uso</a>
                            </label>
                        </div>
                        <div class="text-center">
                            <button type="submit" class="btn btn-rojo">Registrarme</button>
                        </div>
                    </form>

                    <br>

                    <p class="margin-0 text-center">Ya tengo una cuenta <a href="#">Iniciar sesion</a></p>

                </div>
            </div>
        </div>
    </div>

    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="bootstrap/js/bootstrap.js"></script>

</body>
</html>