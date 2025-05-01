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
                    <li class="active">Agregar nuevo producto</li>
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
                    <li role="presentation"><a href="#">Tablero</a></li>
                    <li role="presentation" class="active"><a href="#">Nuevo producto</a></li>
                    <li role="presentation"><a href="#">Mis productos</a></li>
                    <li role="presentation"><a href="#">Vendidos</a></li>
                    <li role="presentation"><a href="#">Comprados</a></li>
                  </ul>

                </div>
              </div>

            </div>

            <div class="col-md-9">

                <div class="page-header margin-0">
                  <h1 class="margin-0">Nuevo producto <small>Agregar nuevo producto</small></h1>
                </div>

                <br>

                <div class="row">

                  <form>

                    <div class="col-md-6">

                        <div class="form-group">
                          <label>Campo de texto</label>
                          <input type="text" class="form-control" placeholder="Texto informativo">
                        </div>

                        <div class="form-group">
                          <label>Campo de texto</label>
                          <input type="text" class="form-control" placeholder="Texto informativo">
                        </div>

                        <div class="form-group">
                          <label>Campo de texto</label>
                          <input type="text" class="form-control" placeholder="Texto informativo">
                        </div>

                        <div class="form-group">
                          <label>Campo de texto</label>
                          <input type="text" class="form-control" placeholder="Texto informativo">
                        </div>

                    </div>

                    <div class="col-md-6">

                        <div class="form-group">
                          <label>Campo de texto</label>
                          <input type="text" class="form-control" placeholder="Texto informativo">
                        </div>

                        <div class="form-group">
                          <label>Campo de texto</label>
                          <input type="text" class="form-control" placeholder="Texto informativo">
                        </div>

                        <div class="form-group">
                          <label>Campo de texto</label>
                          <input type="text" class="form-control" placeholder="Texto informativo">
                        </div>

                        <div class="form-group">
                          <label>Campo de texto</label>
                          <input type="text" class="form-control" placeholder="Texto informativo">
                        </div>

                        <br>

                        <p>
                          <button type="submit" class="btn btn-success">Agregar producto</button>
                          <button type="reset" class="btn btn-default">Limpiar campos</button>
                        </p>

                    </div>

                  </form>

                </div>

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
