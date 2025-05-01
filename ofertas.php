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
                    <li class="active">Ofertas</li>
                </ol>
            </div>
        </div>
    </div>

    <div class="container">
        <div class="row">

            <div class="col-md-3">

            <div class="panel panel-default">
              <div class="panel-heading">
                <h3 class="panel-title">Filtros</h3>
              </div>
              <div class="panel-body">
                <form>
                  <div class="form-group">
                    <label for="exampleInputEmail1">Por fecha</label>
                    <input type="date" class="form-control" id="exampleInputEmail1">
                  </div>
                  <div class="form-group">
                    <label for="exampleInputPassword1">Por categoria</label>
                    <select class="form-control">
                      <option value="" disabled selected>Selecciona una categoria</option>
                      <option value="1">Categoria 1</option>
                      <option value="2">Categoria 2</option>
                      <option value="3">Categoria 3</option>
                      <option value="4">Categoria 4</option>
                    </select>
                  </div>
                  <div class="form-group">
                    <label for="exampleInputFile">Por vendedor</label>
                    <input type="text" class="form-control" id="exampleInputEmail1" placeholder="Nombre del vendedor">
                  </div>
                  <button type="submit" class="btn btn-azul btn-block">Aplicar filtros</button>
                </form>
              </div>
            </div>

            </div>

            <div class="col-md-9">

                <div class="page-header margin-0">
                  <h1 class="margin-0">Ofertas <small>Descubre nuestras ofertas</small></h1>
                </div>

                <br>

                <div class="row">

                  <div class="col-sm-6 col-md-4">
                    <div class="thumbnail">
                      <a href="#"><img src="img/img-default.jpg" alt="Titulo del producto"></a>
                      <div class="caption">
                        <h3 class="margin-5">Aqui va un titulo</h3>
                        <p class="margin-5">Aqui una muy breve descripcion del producto en muestra...</p>
                        <p class="text-center">
                          <a href="#" class="btn btn-azul" role="button">Ver producto</a>
                          <a href="#" class="btn btn-naranja" role="button">Lista de deseos</a>
                        </p>
                      </div>
                    </div>
                  </div>

                  <div class="col-sm-6 col-md-4">
                    <div class="thumbnail">
                      <a href="#"><img src="img/img-default.jpg" alt="Titulo del producto"></a>
                      <div class="caption">
                        <h3 class="margin-5">Aqui va un titulo</h3>
                        <p class="margin-5">Aqui una muy breve descripcion del producto en muestra...</p>
                        <p class="text-center">
                          <a href="#" class="btn btn-azul" role="button">Ver producto</a>
                          <a href="#" class="btn btn-naranja" role="button">Lista de deseos</a>
                        </p>
                      </div>
                    </div>
                  </div>

                  <div class="col-sm-6 col-md-4">
                    <div class="thumbnail">
                      <a href="#"><img src="img/img-default.jpg" alt="Titulo del producto"></a>
                      <div class="caption">
                        <h3 class="margin-5">Aqui va un titulo</h3>
                        <p class="margin-5">Aqui una muy breve descripcion del producto en muestra...</p>
                        <p class="text-center">
                          <a href="#" class="btn btn-azul" role="button">Ver producto</a>
                          <a href="#" class="btn btn-naranja" role="button">Lista de deseos</a>
                        </p>
                      </div>
                    </div>
                  </div>

                  <div class="col-sm-6 col-md-4">
                    <div class="thumbnail">
                      <a href="#"><img src="img/img-default.jpg" alt="Titulo del producto"></a>
                      <div class="caption">
                        <h3 class="margin-5">Aqui va un titulo</h3>
                        <p class="margin-5">Aqui una muy breve descripcion del producto en muestra...</p>
                        <p class="text-center">
                          <a href="#" class="btn btn-azul" role="button">Ver producto</a>
                          <a href="#" class="btn btn-naranja" role="button">Lista de deseos</a>
                        </p>
                      </div>
                    </div>
                  </div>

                  <div class="col-sm-6 col-md-4">
                    <div class="thumbnail">
                      <a href="#"><img src="img/img-default.jpg" alt="Titulo del producto"></a>
                      <div class="caption">
                        <h3 class="margin-5">Aqui va un titulo</h3>
                        <p class="margin-5">Aqui una muy breve descripcion del producto en muestra...</p>
                        <p class="text-center">
                          <a href="#" class="btn btn-azul" role="button">Ver producto</a>
                          <a href="#" class="btn btn-naranja" role="button">Lista de deseos</a>
                        </p>
                      </div>
                    </div>
                  </div>

                  <div class="col-sm-6 col-md-4">
                    <div class="thumbnail">
                      <a href="#"><img src="img/img-default.jpg" alt="Titulo del producto"></a>
                      <div class="caption">
                        <h3 class="margin-5">Aqui va un titulo</h3>
                        <p class="margin-5">Aqui una muy breve descripcion del producto en muestra...</p>
                        <p class="text-center">
                          <a href="#" class="btn btn-azul" role="button">Ver producto</a>
                          <a href="#" class="btn btn-naranja" role="button">Lista de deseos</a>
                        </p>
                      </div>
                    </div>
                  </div>

                </div>

                <div class="text-center">

                  <nav aria-label="Page navigation">
                    <ul class="pagination">
                      <li>
                        <a href="#" aria-label="Previous">
                          <span aria-hidden="true">&laquo;</span>
                        </a>
                      </li>
                      <li><a href="#">1</a></li>
                      <li><a href="#">2</a></li>
                      <li><a href="#">3</a></li>
                      <li><a href="#">4</a></li>
                      <li><a href="#">5</a></li>
                      <li>
                        <a href="#" aria-label="Next">
                          <span aria-hidden="true">&raquo;</span>
                        </a>
                      </li>
                    </ul>
                  </nav>

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
