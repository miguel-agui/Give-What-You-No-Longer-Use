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
                  <li><a href="#">Panel de control</a></li>
                  <li class="active">Tablero</li>
                </ol>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="row">

            <div class="col-md-3">

              <div class="panel panel-default">
                <div class="panel-heading">
                  <h3 class="panel-title">Menú</h3>
                </div>
                <div class="panel-body">

                  <ul class="nav nav-pills nav-stacked">
                    <li role="presentation" class="active"><a href="#">Tablero</a></li>
                    <li role="presentation"><a href="#">Nuevo producto</a></li>
                    <li role="presentation"><a href="#">Mis productos</a></li>
                    <li role="presentation"><a href="#">Vendidos</a></li>
                    <li role="presentation"><a href="#">Comprados</a></li>
                  </ul>

                </div>
              </div>

            </div>

            <div class="col-md-9">

                <div class="page-header margin-0">
                  <h1 class="margin-0">Tablero <small>Ultimos detalles de cuenta</small></h1>
                </div>

                <br>

                <h1>Aqui pondre algunas estadisticas importantes...</h1>
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
