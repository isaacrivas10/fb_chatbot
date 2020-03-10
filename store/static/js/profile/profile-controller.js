 
$(".sidebar-dropdown > a").click(
  function() {
    $(".sidebar-submenu").slideUp(200);
    if ($(this).parent().hasClass("active")) {
      $(".sidebar-dropdown").removeClass("active");
      $(this).parent().removeClass("active");
    } else {
      $(".sidebar-dropdown").removeClass("active");
      $(this).next(".sidebar-submenu").slideDown(200);
      $(this).parent().addClass("active");
    }
  }
);
$("#close-sidebar").click(
  function() {
    $(".page-wrapper").removeClass("toggled");
  }
);
$("#show-sidebar").click(
  function(ev) {
    $(".page-wrapper").addClass("toggled");
    ev.preventDefault();
    ev.stopPropagation();
  }
);
function closeAlert(){
  $('#alert').hide();
}

// Aqui se cargan todas las funciones que actualizan el html
load= {
  profileDashboard: ()=>{
    $('#main-profile').empty();
    facebook=false;twitter=false;
    if(userData.socialMedia.facebook){
      facebook= '<a href="'+userData.socialMedia.facebook+'" class="fab fab-a fa-facebook"></a>'
    }
    if(userData.socialMedia.twitter){
      twitter= '<a href="'+userData.socialMedia.twitter+'" class="fab fab-a fa-twitter"></a>'
    }
    $('#main-profile').html(
    `<div class="row">
    <div class="col-lg-4 text-center">
      <div>
        <img class="img-fluid w-50 h-50 rounded-circle border-white" src="${'../ajax/'+userData.photo}" alt="user img">
      </div>
      <div class="pre-card text-center">
        <div class="card-body">
          <h4 class="card-title">${userData.name.first} ${userData.name.last}</h4>
          <p class="card-text">
            <ul>
              <li>
                <i class="fas fa-briefcase"></i> Ocupacion
              </li>
              <li>
                <i class="fa fa-map-marker"></i> Ubicacion
              </li>
            </ul>
          </p>                  
        </div>
        <div class="container text-left">
            <h6 >ABOUT</h6>
            <p>${userData.about}
            </p>
        </div>
        <div class="container text-left">
            <h6>Connect</h6>
            ${facebook? facebook:''}
            ${twitter? twitter:''}
        </div>
      </div>
    </div>
    <div class="col-lg-8">
      <div class="d-flex align-items-center p-3 my-3 text-white-50 bg-dark rounded shadow-sm">
        <div class="lh-100">
          <h6 class="mb-0 text-white lh-100">Profile Overview</h6>
        </div>
      </div>
      <div class="my-3 p-3 bg-white rounded shadow-sm">
        <h6 class="border-bottom border-gray pb-2 mb-0">Recent updates</h6>
        <div class="media text-muted pt-3">
          <p class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
            <strong class="d-block text-gray-dark">Tuesday </strong>
            Posted a product
          </p>
        </div>
        
        <small class="d-block text-right mt-3">
          <a href="#">All updates</a>
        </small>
      </div>
    </div>
  </div>`);
  },
  products: ()=>{
    $('#main-profile').empty();
    $('#main-profile').html(`<div class="my-3 p-3 bg-white rounded shadow-sm">
      <div class=" d-flex flex-row border-bottom border-gray pb-0 mb-3">
          <h6 class="">All My Products</h6>
          <small class="ml-auto">
              <a href="#" data-toggle="modal" data-target="#productModal">New Product</a>
          </small>
      </div>
      <div id="products" class="row mb-2"></div>`
      );
    prd= ajax(
      'GET',
      '../ajax/',
      'id='+userID,
      function(res){
        console.log(res);
      },
      function error(e){
        console.log(e);
      }
    );
    for (let i=0; i<prd.length; i++){
      $('#products').append(
        `<div class="col-md-6 ">
          <div class="row no-gutters border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-250 position-relative">
            <div class="col-lg-6 col-md-12 col-sm-6 p-4 d-flex flex-column position-static">
              <strong class="d-inline-block mb-2 text-primary">Category</strong>
              <h3 class="mb-0">Product Name</h3>
              <div class="mb-1 text-muted">Price</div>
              <p class="card-text mb-auto">This is a wider card with supporting text below as a natural lead-in to additional content.</p>
            </div>
            <div class="col-lg-6 col-md-12 col-sm-6 img-full">
              <img src="../img/bmw.jpg" alt="" class="img-fluid">
            </div>
            <div class="col-lg-12 text-right ">
              <a href="#" class="stretched-link mr-2" data-toggle="modal" data-target="#productModal">Edit Product</a>
            </div>                       
          </div>             
        </div>`
        );
    }
  },
  orders: ()=>{
    $('#main-profile').empty();
    $('#main-profile').html(
      `<div class="d-flex align-items-center p-3 my-3 text-white-50 bg-dark rounded shadow-sm">
          <div class="lh-100">
            <h6 class="mb-0 text-white lh-100">Sketched Orders</h6>
          </div>
        </div>
        <div id="orders" class="my-3 p-3 bg-white rounded shadow-sm">
          <h6 class="border-bottom border-gray pb-2 mb-0">Recent Orders</h6>
        </div>`
      );
    for (let i=0; i<10; i++){
      $('#orders').append(
        `<div class="media text-muted pt-3">
          <div class="media-body pb-3 mb-0 small lh-125 border-bottom border-gray">
            <p>
            <strong class="text-gray-dark">@username </strong>bought a product: <br>
              &nbsp;&nbsp;<strong class="text-gray-dark">Product Name: </strong>name <br>
              &nbsp;&nbsp;<strong class="text-gray-dark">Quantity: </strong>number <br>
              &nbsp;&nbsp;<strong class="text-gray-dark">Total: </strong>total <br>
            </p>
            <small class="d-block text-right mt-3">
                <a href="">Complete Details</a>
            </small>
          </div>
        </div>`
      );
    }
    $('#orders').append(
      `<small class="text-right mt-3">
        <p>Last</p>
      </small>`);
  },
  map: ()=>{
    $('#main-profile').empty();
    $('#main-profile').html(
      `<div class="card mb-3">
        <div class="d-flex justify-content-between card-header">
          <div class="align-self-center">  
        <i class="fa fa-map"></i>
          Google Maps Visualization</div>
          <div><button onclick="getLocation()" class="btn btn-primary mr-auto">Set Location</button></div>
        </div>
        <div id="alert" class="alert alert-warning collapse" role="alert">
          <strong>Holy guacamole!</strong>
          There was a problem getting your location. Refresh and try again.
          <button type="button" onclick="closeAlert()" class="close">
            <span id="close-btn" aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="card-body">
          <div id="map" class="container-fluid rounded">
            <div class="d-flex align-items-center text-primary">
              <strong>Loading...</strong>
              <div class="spinner-border ml-auto" role="status" aria-hidden="true"></div>
            </div>
          </div>
        </div>
        <div class="card-footer small text-muted">
          Map Updated
        </div>
      </div> `
      );      
    var head= document.getElementsByTagName('head')[0];
    var script= document.createElement('script');
    script.id= "google-maps";
    script.async= true;
    script.defer= true;
    script.src= "https://maps.googleapis.com/maps/api/js?key=AIzaSyCxvGODTgLbBAiG5XQR-M886o1XsIHJmFo&callback=initMap";
    $("#close-sidebar").trigger('click');
    setTimeout(
      function(){
        head.appendChild(script);
        $('#map').addClass('map-size');
      }, 800
    );
  },
  chart: (chart)=>{
    $('#main-profile').empty();
    $('#main-profile').html(
      `<div id="charts" class="container-fluid">
        <ol class="breadcrumb bg-dark ">
          <li class="breadcrumb-item">
            <a class="text-white" href="#">Dashboard</a>
          </li>
          <li class="breadcrumb-item active">Charts</li>
        </ol>
        <div class="card mb-3">
          <div class="card-header">
            <i class="fas fa-chart-${chart}"></i>
            ${chart[0].toUpperCase()+chart.slice(1)} Chart</div>
          <div class="card-body">
            <canvas id="${chart}Chart" width="100%" height="30"></canvas>
          </div>
          <div class="card-footer small text-muted">Updated yesterday at 11:59 PM</div>
        </div>
      </div>`);
    chartFunctions[chart]();
  },
  configuration: ()=> {
    $('#main-profile').empty();
    $('#main-profile').html(
      `<div class="col-lg-12">
      <div class="d-flex align-items-center p-3 my-3 text-white-50 bg-dark rounded shadow-sm">
        <div class="lh-100">
          <h6 class="mb-0 text-white lh-100">Profile General Information</h6>
        </div>
      </div>
      <div class="my-3 p-3 bg-white rounded shadow-sm">
          <form class="p-4" >
            <div class="form-row mb-2">
              <div class="col-lg-6 col-md-12 text-center mb-3">
                <div class="mb-2">
                  <img src="${'../ajax/'+userData.photo}" id='usr-img' alt="user img" class="img-fluid w-50 h-50">
                </div>
                <div class="col-10 custom-file">
                  <input id="new-img-btn" type="file" class="custom-file-input" id="fileInput" aria-describedby="fileInput">
                  <label class="custom-file-label text-left" for="fileInput">Image</label>
                  <div class="invalid-feedback">Please choose an image</div>
                </div>
              </div>
              <div class="col-lg-6 col-md-12">
                <div class="form-group ">
                  <label for="firstName">First Name</label>
                  <input value="${userData.name.first}" type="text" class="form-control" id="firstName" placeholder="First Name">
                </div>
                <div class="form-group ">
                  <label for="lastName">Last Name</label>
                  <input value="${userData.name.last}" type="text" class="form-control" id="lastName" placeholder="Last Name">
                </div>
                <div class="form-group col-10">
                  <label for="inputPhone">Phone</label>
                  <input value="${userData.phone}" type="number" class="form-control" id="inputPhone">
                </div>
              </div>
            </div>
             
            <div class="form-row">
              <div class="form-group col-md-6">
                <label for="inputEmail4">Email</label>
                <input value="${userData.email}" type="email" class="form-control" id="inputEmail4" placeholder="Email">
              </div>
              <div class="form-group col-md-6">
                <label for="inputPassword4">Password</label>
                <input type="password" class="form-control" id="inputPassword4" placeholder="Password">
              </div>
            </div>
            <div class="form-row">
              <div class="col-lg-4 col-md-4 col-sm-12">
                <label class="sr-only" for="facebook">Facebook</label>
                <div class="input-group mb-2">
                  <div class="input-group-prepend">
                    <div class="input-group-text"><i class="fab fa-facebook "></i></div>
                  </div>
                  <input value="${userData.socialMedia.facebook}" type="text" class="form-control" id="facebook" placeholder="Facebook">
                </div>
              </div>
              <div class="col-lg-4 col-md-4 col-sm-12">
                <label class="sr-only" for="twitter">Twitter</label>
                <div class="input-group mb-2">
                  <div class="input-group-prepend">
                    <div class="input-group-text"><i class="fab fa-twitter"></i></div>
                  </div>
                  <input value="${userData.socialMedia.twitter}" type="text" class="form-control" id="twitter" placeholder="Username">
                </div>
              </div>
              <div class="col-lg-4 col-md-4 col-sm-12">
                <label class="sr-only" for="whatsapp">WhatsApp</label>
                <div class="input-group mb-2">
                  <div class="input-group-prepend">
                    <div class="input-group-text"><i class="fab fa-whatsapp"></i></div>
                  </div>
                  <input value="${userData.socialMedia.twitter}" type="text" class="form-control" id="whatsapp" placeholder="WhatsApp">
                </div>
              </div>
            </div>
            <button type="submit" class="btn btn-primary text-right">Save</button>
          </form>
      </div>
    </div>`);
  }
};


function loadContent(){
  $('#userName').html(userData.name.first + ' ' +userData.name.last);
  $('#usr-pic').attr('src', '../ajax/'+userData.photo);
  if(userData.accountType == "admin"){
    $('#role').html('Administrator');
    $('#ecommerce').addClass('invisible');
    $('#charts').addClass('invisible');
  }
  if(userData.accountType == 'customer'){
    $('#role').html('Customer');
    $('#prd').addClass('invisible');
    $('#components').addClass('invisible');
    $('#charts').addClass('invisible');
  }
  if(userData.accountType == 'enterprise'){
    $('#role').html('Enterprise');
    $('#components').addClass('invisible');
    $('#charts').addClass('invisible');
  }
}

function logOut(){
  deleteCookie('sessionID');
  window.location.href="../index.html";
}

$(document).ready(
  function(){
    $("#close-sidebar").trigger('click');
    $("#new-img-btn").on('change',function (){
      console.log('trash');
      //loadImg($(this), $('#usr-img'));
    });

    $('#productForm').submit(
      function(e){
          e.preventDefault();
          setProduct($(this).serialize());
      })
  }
)
