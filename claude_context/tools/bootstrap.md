### NPM Script for Starting Vite

Source: https://getbootstrap.com/docs/5.3/getting-started/vite

Defines the 'start' script in `package.json` to run the Vite development server. This script is used to launch the local server for development and hot reloading.

```json
{
  // ...
  "scripts": {
    "start": "vite",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  // ...
}

```

--------------------------------

### Start Parcel Development Server

Source: https://getbootstrap.com/docs/5.3/getting-started/parcel

Executes the 'start' npm script to launch the Parcel development server. This command compiles the project's assets and makes the application accessible locally, allowing for real-time development and testing.

```bash
npm start

```

--------------------------------

### Install Bootstrap and Popper.js

Source: https://getbootstrap.com/docs/5.3/getting-started/vite

Installs Bootstrap and its dependency Popper.js. Bootstrap provides the UI framework, while Popper.js is essential for the positioning of components like dropdowns, popovers, and tooltips.

```bash
npm i --save bootstrap @popperjs/core
```

--------------------------------

### Add Parcel Start Script to package.json

Source: https://getbootstrap.com/docs/5.3/getting-started/parcel

Adds a 'start' script to the package.json file to launch the Parcel development server. This script serves the specified HTML file, compiles assets, and outputs them to a 'dist' directory. It simplifies the process of running the project locally.

```json
{
   // ...
   "scripts": {
     "start": "parcel serve src/index.html --public-url / --dist-dir dist",
     "test": "echo \"Error: no test specified\" && exit 1"
   },
   // ...
}

```

--------------------------------

### Bootstrap Three Equal Columns Example (md)

Source: https://getbootstrap.com/docs/5.3/examples/grid

Creates three equal-width columns that start at the medium (md) breakpoint and scale up. On smaller viewports, these columns will stack automatically.

```html
.col-md-4
.col-md-4
.col-md-4
```

--------------------------------

### Initialize npm Project with Parcel

Source: https://getbootstrap.com/docs/5.3/getting-started/parcel

Creates a new project folder and initializes npm with default settings. This sets up the project for dependency management. No specific inputs or outputs are detailed, but it prepares the environment for subsequent installations.

```bash
mkdir my-project && cd my-project
npm init -y

```

--------------------------------

### Bootstrap 5.3 JavaScript and Popper.js via CDN (Separate)

Source: https://getbootstrap.com/docs/5.3/getting-started/introduction

This snippet shows how to include Bootstrap's JavaScript and Popper.js separately via CDN. This approach is useful if you do not require dropdowns, popovers, or tooltips, allowing for a smaller download size by omitting Popper.

```javascript
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.min.js" integrity="sha384-G/EV+4j2dNv+tEPo3++6LCgdCROaejBqfUeNjuKAiuXbjrxilcCdDz6ZAVfHWe1Y" crossorigin="anonymous"></script>

```

--------------------------------

### Bootstrap 5.3 HTML with CSS and JS via CDN

Source: https://getbootstrap.com/docs/5.3/getting-started/introduction

This code demonstrates how to include Bootstrap 5.3's production-ready CSS and JavaScript bundles using CDN links. The CSS is placed in the `<head>` and the JavaScript bundle (including Popper) is placed before the closing `</body>` tag for optimal performance.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-sRIl4kxILFvY47J16cr9ZwB07vP4J8+LH7qKQnuqkuIAvNWLzeN8tE5YBujZqJLB" crossorigin="anonymous">
  </head>
  <body>
    <h1>Hello, world!</h1>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>
  </body>
</html>

```

--------------------------------

### Basic HTML Structure for Bootstrap

Source: https://getbootstrap.com/docs/5.3/getting-started/introduction

This snippet shows the essential HTML structure for a Bootstrap page, including the viewport meta tag for responsive behavior. It serves as a foundational template before including Bootstrap's CSS and JavaScript.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap demo</title>
  </head>
  <body>
    <h1>Hello, world!</h1>
  </body>
</html>

```

--------------------------------

### Install Bootstrap and Popper.js

Source: https://getbootstrap.com/docs/5.3/getting-started/parcel

Installs Bootstrap and its dependency Popper.js for positioning components like dropdowns and tooltips. If these components are not used, Popper.js can be omitted. This command adds essential libraries for UI development.

```bash
npm i --save bootstrap @popperjs/core

```

--------------------------------

### Install Development Dependencies for Parcel

Source: https://getbootstrap.com/docs/5.3/getting-started/parcel

Installs Parcel as a development dependency. Parcel automatically detects and installs necessary language transformers, such as Sass. This command ensures Parcel is available for local development.

```bash
npm i --save-dev parcel

```

--------------------------------

### Compile CSS, JS, and Start Local Server with npm

Source: https://getbootstrap.com/docs/5.3/getting-started/contribute

This npm script compiles the project's CSS and JavaScript, builds the documentation, and then starts a local development server. It's a primary task for active development.

```bash
npm start
```

--------------------------------

### Define npm Scripts: package.json

Source: https://getbootstrap.com/docs/5.3/getting-started/webpack

Adds npm scripts to the `package.json` file for managing the project. The `start` script launches the Webpack development server for local development with hot reloading, and the `build` script compiles the project in production mode. These scripts streamline the development workflow.

```json
{
  // ...
  "scripts": {
    "start": "webpack serve",
    "build": "webpack build --mode=production",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  // ...
}
```

--------------------------------

### Install Vite as Dev Dependency

Source: https://getbootstrap.com/docs/5.3/getting-started/vite

Installs Vite, a modern frontend build tool, as a development dependency. This command ensures Vite is available for development and build processes but not included in the production bundle.

```bash
npm i --save-dev vite
```

--------------------------------

### Run Bootstrap Documentation Locally

Source: https://getbootstrap.com/docs/5.3/getting-started/contribute

This command compiles and serves the Bootstrap documentation locally, allowing developers to preview changes. It requires Node.js and all dependencies to be installed via 'npm install'.

```bash
npm run docs-serve
```

--------------------------------

### Install Webpack development dependencies

Source: https://getbootstrap.com/docs/5.3/getting-started/webpack

Installs core Webpack packages and the HTML Webpack Plugin as development dependencies. These include webpack, webpack-cli for terminal commands, webpack-dev-server for a local server, and html-webpack-plugin for managing index.html.

```bash
npm i --save-dev webpack webpack-cli webpack-dev-server html-webpack-plugin
```

--------------------------------

### Bootstrap Two Columns Example (md)

Source: https://getbootstrap.com/docs/5.3/examples/grid

Sets up two columns with predefined widths that begin at the medium (md) breakpoint. On smaller screens, these columns will stack.

```html
.col-md-8
.col-md-4
```

--------------------------------

### Install Local Dependencies with npm

Source: https://getbootstrap.com/docs/5.3/getting-started/contribute

This command installs all the necessary local dependencies for developing Bootstrap, as defined in the project's package.json file. It should be run from the root '/bootstrap' directory after cloning or downloading the source files.

```bash
npm install
```

--------------------------------

### Bootstrap Three Unequal Columns Example (md)

Source: https://getbootstrap.com/docs/5.3/examples/grid

Demonstrates creating three columns of varying widths that start at the medium (md) breakpoint. The sum of column widths should ideally be twelve for a single horizontal block.

```html
.col-md-3
.col-md-6
.col-md-3
```

--------------------------------

### Install Bootstrap with RubyGems

Source: https://getbootstrap.com/docs/5.3/getting-started/download

Installs Bootstrap using RubyGems. It is recommended to use Bundler by adding the gem to your Gemfile, or install directly using the `gem install` command.

```ruby
gem 'bootstrap', '~> 5.3.8'
```

```shell
gem install bootstrap -v 5.3.8
```

--------------------------------

### Install Sass for CSS Preprocessing

Source: https://getbootstrap.com/docs/5.3/getting-started/vite

Installs Sass as a development dependency. Sass is a CSS preprocessor that allows for more advanced styling, including variables, nesting, and mixins, which are used for importing and bundling Bootstrap's CSS.

```bash
npm i --save-dev sass
```

--------------------------------

### Install mini-css-extract-plugin

Source: https://getbootstrap.com/docs/5.3/getting-started/webpack

Installs the mini-css-extract-plugin as a development dependency using npm. This plugin is essential for extracting CSS into separate files instead of bundling it with JavaScript.

```bash
npm install --save-dev mini-css-extract-plugin

```

--------------------------------

### Initialize npm Project

Source: https://getbootstrap.com/docs/5.3/getting-started/vite

Initializes a new npm project in a specified directory. This command creates a package.json file with default settings, preparing the project for package management.

```bash
mkdir my-project && cd my-project
npm init -y
```

--------------------------------

### Bootstrap Mixed Grid Example (Mobile, Tablet, Desktop)

Source: https://getbootstrap.com/docs/5.3/examples/grid

A more complex responsive layout example combining classes for mobile (sm), tablet, and desktop viewports. This allows for granular control over column widths at different screen sizes.

```html
.col-sm-6 .col-lg-8
.col-6 .col-lg-4
.col-6 .col-sm-4
.col-6 .col-sm-4
.col-6 .col-sm-4
```

--------------------------------

### Install Sass and Webpack loaders

Source: https://getbootstrap.com/docs/5.3/getting-started/webpack

Installs additional development dependencies for processing Sass files and integrating them with Webpack. This includes autoprefixer, css-loader, postcss-loader, sass, sass-loader, and style-loader.

```bash
npm i --save-dev autoprefixer css-loader postcss-loader sass sass-loader style-loader
```

--------------------------------

### Install Bootstrap with NuGet

Source: https://getbootstrap.com/docs/5.3/getting-started/download

Installs Bootstrap CSS or Sass and JavaScript for .NET Framework projects using the NuGet package manager. Note that NuGet is primarily for compiled code.

```powershell
Install-Package bootstrap
Install-Package bootstrap.sass
```

--------------------------------

### HTML5 Doctype Declaration for Bootstrap

Source: https://getbootstrap.com/docs/5.3/getting-started/introduction

Bootstrap requires the HTML5 doctype for correct and complete styling. This declaration ensures that browsers render the page according to modern web standards.

```html
<!doctype html>
<html lang="en">
  ...
</html>

```

--------------------------------

### Bootstrap CSS Grid: Start Classes for Alignment (HTML)

Source: https://getbootstrap.com/docs/5.3/layout/css-grid

This example illustrates the use of 'start' classes in Bootstrap's CSS Grid for aligning columns. The `.g-start-2` class specifies that the column should begin at the second grid line, and `.g-col-3` defines its width.

```html
<div class="grid text-center">
  <div class="g-col-3 g-start-2">.g-col-3 .g-start-2</div>
  <div class="g-col-4 g-start-6">.g-col-4 .g-start-6</div>
</div>

```

--------------------------------

### Install Bootstrap with Bun

Source: https://getbootstrap.com/docs/5.3/getting-started/download

Installs Bootstrap version 5.3.8 using the Bun package manager, suitable for Bun or Node.js applications.

```shell
bun add bootstrap@5.3.8
```

--------------------------------

### HTML Table Example in Bootstrap

Source: https://getbootstrap.com/docs/5.3/examples/blog

Shows a basic HTML table styled with Bootstrap. This example includes a header row and data rows, demonstrating Bootstrap's default table styling for readability. It uses standard HTML table markup.

```html
Name | Upvotes | Downvotes
---|---|---
Alice | 10 | 11
Bob | 4 | 3
Charlie | 7 | 9
Totals | 21 | 23
```

--------------------------------

### Install Bootstrap with Composer

Source: https://getbootstrap.com/docs/5.3/getting-started/download

Installs Bootstrap's Sass and JavaScript assets using Composer, a dependency manager for PHP.

```shell
composer require twbs/bootstrap:5.3.8
```

--------------------------------

### Create Project Structure

Source: https://getbootstrap.com/docs/5.3/getting-started/parcel

Sets up the necessary directories and files for the project structure, including source folders for JavaScript and SCSS, and an HTML entry point. This command organizes the project for Parcel to process.

```bash
mkdir {src,src/js,src/scss}
touch src/index.html src/js/main.js src/scss/styles.scss

```

--------------------------------

### Basic Bootstrap Card Example

Source: https://getbootstrap.com/docs/5.3/components/card

Demonstrates a basic Bootstrap card with an image, title, text, and a button. Cards are responsive and fill parent width by default, requiring spacing utilities for margins. This example uses a fixed width for illustration.

```html
<div class="card" style="width: 18rem;">
  <img src="..." class="card-img-top" alt="...">
  <div class="card-body">
    <h5 class="card-title">Card title</h5>
    <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card’s content.</p>
    <a href="#" class="btn btn-primary">Go somewhere</a>
  </div>
</div>
```

--------------------------------

### Example Code Block in Bootstrap

Source: https://getbootstrap.com/docs/5.3/examples/blog

Demonstrates a simple code block using Bootstrap styling. It's intended to show how preformatted code is displayed within a blog post context. No specific libraries or frameworks are required beyond Bootstrap's CSS.

```plaintext
Example code block
```

--------------------------------

### Install Bootstrap 5.3.8 with npm (CLI)

Source: https://getbootstrap.com/docs/5.3/getting-started/download

Install Bootstrap version 5.3.8 into your Node.js project using npm. This command fetches the package and makes its source files available for your build process. Requires npm to be installed.

```bash
npm install bootstrap@5.3.8

```

--------------------------------

### Bootstrap Combined Gutters Example

Source: https://getbootstrap.com/docs/5.3/examples/grid

Illustrates adjusting both horizontal and vertical gutters simultaneously using the `.g-*` classes. This example uses `.g-3` for consistent spacing in both directions.

```html
`.col` with `.g-3` gutters
`.col` with `.g-3` gutters
`.col` with `.g-3` gutters
`.col` with `.g-3` gutters
`.col` with `.g-3` gutters
`.col` with `.g-3` gutters
```

--------------------------------

### Bootstrap Horizontal Gutters Example

Source: https://getbootstrap.com/docs/5.3/examples/grid

Demonstrates adjusting horizontal gutters between columns using the `.gx-*` classes. This example applies `.gx-4` to create consistent spacing between columns.

```html
`.col` with `.gx-4` gutters
`.col` with `.gx-4` gutters
`.col` with `.gx-4` gutters
`.col` with `.gx-4` gutters
`.col` with `.gx-4` gutters
`.col` with `.gx-4` gutters
```

--------------------------------

### Bootstrap Mixed Grid Example (Mobile and Desktop)

Source: https://getbootstrap.com/docs/5.3/examples/grid

Shows a flexible layout using a combination of Bootstrap's grid classes for different viewports (md and down). It demonstrates how columns can adapt from desktop to mobile.

```html
.col-md-8
.col-6 .col-md-4
.col-6 .col-md-4
.col-6 .col-md-4
.col-6 .col-md-4
.col-6
.col-6
```

--------------------------------

### Bootstrap Container Examples

Source: https://getbootstrap.com/docs/5.3/examples/grid

Provides examples of different container classes in Bootstrap, which define the maximum width of the content area. Includes fluid containers and breakpoint-specific containers.

```html
.container
.container-sm
.container-md
.container-lg
.container-xl
.container-xxl
.container-fluid
```

--------------------------------

### Bootstrap Three Equal Columns Alternative (md)

Source: https://getbootstrap.com/docs/5.3/examples/grid

An alternative method to create a grid with three equal columns starting at the medium (md) breakpoint using `.row-cols-*` classes. Child `.col` elements will equally divide the row.

```html
`.col` child of `.row-cols-md-3`
`.col` child of `.row-cols-md-3`
`.col` child of `.row-cols-md-3`
```

--------------------------------

### Viewport Meta Tag for Responsive Design

Source: https://getbootstrap.com/docs/5.3/getting-started/introduction

To ensure proper rendering and touch zooming across all devices, especially in a mobile-first approach, Bootstrap recommends including this responsive viewport meta tag in the HTML head.

```html
<meta name="viewport" content="width=device-width, initial-scale=1">

```

--------------------------------

### Install Bootstrap with Yarn

Source: https://getbootstrap.com/docs/5.3/getting-started/download

Installs Bootstrap version 5.3.8 using the Yarn package manager. For Yarn 2+, specific configurations are required to manage dependencies.

```shell
yarn add bootstrap@5.3.8
yarn config set nodeLinker node-modules
touch yarn.lock
yarn install
yarn start
```

--------------------------------

### Create Project Structure

Source: https://getbootstrap.com/docs/5.3/getting-started/vite

Creates the necessary directories and files for the project structure. This includes folders for source files (src), JavaScript (src/js), SCSS (src/scss), and essential configuration files like index.html, main.js, styles.scss, and vite.config.js.

```bash
mkdir {src,src/js,src/scss}
touch src/index.html src/js/main.js src/scss/styles.scss vite.config.js
```

--------------------------------

### Bootstrap Link Example (HTML)

Source: https://getbootstrap.com/docs/5.3/content/reboot

Shows a basic example of a link in Bootstrap, which has default color and underline styling. It also demonstrates how to adjust the link's opacity using CSS variables.

```html
<a href="#">This is an example link</a>

```

```html
<a href="#" style="--bs-link-opacity: .5">This is an example link</a>

```

--------------------------------

### Bootstrap Offcanvas Component Example (HTML)

Source: https://getbootstrap.com/docs/5.3/components/offcanvas

This snippet demonstrates a basic Offcanvas component with a header, close button, and body content. It is configured to be shown by default using the `.show` class.

```html
<div class="offcanvas offcanvas-start show" tabindex="-1" id="offcanvas" aria-labelledby="offcanvasLabel">
  <div class="offcanvas-header">
    <h5 class="offcanvas-title" id="offcanvasLabel">Offcanvas</h5>
    <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
  </div>
  <div class="offcanvas-body">
    Content for the offcanvas goes here. You can place just about any Bootstrap component or custom elements here.
  </div>
</div>
```

--------------------------------

### Bootstrap Grid System Tiers Example

Source: https://getbootstrap.com/docs/5.3/examples/grid

Demonstrates the five tiers of the Bootstrap grid system (xs, sm, md, lg, xl, xxl). Each tier applies to a minimum viewport size and scales up unless overridden. This example shows classes for each tier.

```html
.col-4
.col-4
.col-4
.col-sm-4
.col-sm-4
.col-sm-4
.col-md-4
.col-md-4
.col-md-4
.col-lg-4
.col-lg-4
.col-lg-4
.col-xl-4
.col-xl-4
.col-xl-4
.col-xxl-4
.col-xxl-4
.col-xxl-4
```

--------------------------------

### Bootstrap Input Group Basic Examples

Source: https://getbootstrap.com/docs/5.3/forms/input-group

Demonstrates various ways to use Bootstrap input groups with text or buttons on one or both sides of input fields, including examples with textareas and custom URLs.

```html
<div class="input-group mb-3">
  <span class="input-group-text" id="basic-addon1">@</span>
  <input type="text" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="basic-addon1">
</div>

<div class="input-group mb-3">
  <input type="text" class="form-control" placeholder="Recipient’s username" aria-label="Recipient’s username" aria-describedby="basic-addon2">
  <span class="input-group-text" id="basic-addon2">@example.com</span>
</div>

<div class="mb-3">
  <label for="basic-url" class="form-label">Your vanity URL</label>
  <div class="input-group">
    <span class="input-group-text" id="basic-addon3">https://example.com/users/</span>
    <input type="text" class="form-control" id="basic-url" aria-describedby="basic-addon3 basic-addon4">
  </div>
  <div class="form-text" id="basic-addon4">Example help text goes outside the input group.</div>
</div>

<div class="input-group mb-3">
  <span class="input-group-text">$</span>
  <input type="text" class="form-control" aria-label="Amount (to the nearest dollar)">
  <span class="input-group-text">.00</span>
</div>

<div class="input-group mb-3">
  <input type="text" class="form-control" placeholder="Username" aria-label="Username">
  <span class="input-group-text">@</span>
  <input type="text" class="form-control" placeholder="Server" aria-label="Server">
</div>

<div class="input-group">
  <span class="input-group-text">With textarea</span>
  <textarea class="form-control" aria-label="With textarea"></textarea>
</div>
```

--------------------------------

### Bootstrap Pagination: Small Size Example (HTML)

Source: https://getbootstrap.com/docs/5.3/components/pagination

Illustrates how to create a small-sized Bootstrap pagination component using the `.pagination-sm` class. This reduces the padding and font size of the pagination items.

```html
<nav aria-label="...">
  <ul class="pagination pagination-sm">
    <li class="page-item active">
      <a class="page-link" aria-current="page">1</a>
    </li>
    <li class="page-item"><a class="page-link" href="#">2</a></li>
    <li class="page-item"><a class="page-link" href="#">3</a></li>
  </ul>
</nav>
```

--------------------------------

### Bootstrap CSS Grid: Responsive Layout (HTML)

Source: https://getbootstrap.com/docs/5.3/layout/css-grid

This example showcases how to create a responsive layout using Bootstrap's CSS Grid. It starts with two columns on smaller viewports (`.g-col-6`) and transitions to three columns on medium viewports and above (`.g-col-md-4`).

```html
<div class="grid text-center">
  <div class="g-col-6 g-col-md-4">.g-col-6 .g-col-md-4</div>
  <div class="g-col-6 g-col-md-4">.g-col-6 .g-col-md-4</div>
  <div class="g-col-6 g-col-md-4">.g-col-6 .g-col-md-4</div>
</div>

```

--------------------------------

### Bootstrap Vertical Gutters Example

Source: https://getbootstrap.com/docs/5.3/examples/grid

Shows how to control vertical spacing between rows of columns using the `.gy-*` classes. This example utilizes `.gy-4` for uniform vertical gutters.

```html
`.col` with `.gy-4` gutters
`.col` with `.gy-4` gutters
`.col` with `.gy-4` gutters
`.col` with `.gy-4` gutters
`.col` with `.gy-4` gutters
`.col` with `.gy-4` gutters
```

--------------------------------

### Create Bootstrap and Webpack project structure

Source: https://getbootstrap.com/docs/5.3/getting-started/webpack

Creates the necessary directories and files for a Bootstrap and Webpack project. This includes 'src' and 'src/js', 'src/scss' directories, and empty files for index.html, main.js, styles.scss, and webpack.config.js.

```bash
mkdir {src,src/js,src/scss}
touch src/index.html src/js/main.js src/scss/styles.scss webpack.config.js
```

--------------------------------

### Basic Form Example with Bootstrap

Source: https://getbootstrap.com/docs/5.3/forms/overview

Demonstrates a standard Bootstrap form with email, password, and checkbox inputs, along with a submit button. It utilizes Bootstrap's form classes for styling and includes an example of help text for an input.

```html
<form>
  <div class="mb-3">
    <label for="exampleInputEmail1" class="form-label">Email address</label>
    <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
    <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
  </div>
  <div class="mb-3">
    <label for="exampleInputPassword1" class="form-label">Password</label>
    <input type="password" class="form-control" id="exampleInputPassword1">
  </div>
  <div class="mb-3 form-check">
    <input type="checkbox" class="form-form-check-input" id="exampleCheck1">
    <label class="form-check-label" for="exampleCheck1">Check me out</label>
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

--------------------------------

### Importing Specific Bootstrap Sass Parts

Source: https://getbootstrap.com/docs/5.3/customize/sass

Provides an example of selectively importing Bootstrap's Sass files to reduce build size and include only necessary components. It outlines the recommended order of imports, starting with functions and variables.

```scss
// Custom.scss
// Option B: Include parts of Bootstrap

// 1. Include functions first (so you can manipulate colors, SVGs, calc, etc)
@import "../node_modules/bootstrap/scss/functions";

// 2. Include any default variable overrides here

// 3. Include remainder of required Bootstrap stylesheets (including any separate color mode stylesheets)
@import "../node_modules/bootstrap/scss/variables";
@import "../node_modules/bootstrap/scss/variables-dark";

// 4. Include any default map overrides here

// 5. Include remainder of required parts
@import "../node_modules/bootstrap/scss/maps";
@import "../node_modules/bootstrap/scss/mixins";
@import "../node_modules/bootstrap/scss/root";

// 6. Include any other optional stylesheet partials as desired; list below is not inclusive of all available stylesheets
@import "../node_modules/bootstrap/scss/utilities";
@import "../node_modules/bootstrap/scss/reboot";
@import "../node_modules/bootstrap/scss/type";
@import "../node_modules/bootstrap/scss/images";
@import "../node_modules/bootstrap/scss/containers";
@import "../node_modules/bootstrap/scss/grid";
@import "../node_modules/bootstrap/scss/helpers";
// ...

// 7. Optionally include utilities API last to generate classes based on the Sass map in `_utilities.scss`
@import "../node_modules/bootstrap/scss/utilities/api";

// 8. Add additional custom code here

```

--------------------------------

### Bootstrap Horizontal Rule Examples (HTML)

Source: https://getbootstrap.com/docs/5.3/content/reboot

Provides examples of horizontal rules (`<hr>`) in Bootstrap. These are styled with `border-top`, default opacity, and inherit their color from the parent. Examples show default usage, colored variants, and customization with border and opacity utilities.

```html
<hr>

<div class="text-success">
  <hr>
</div>

<hr class="border border-danger border-2 opacity-50">
<hr class="border border-primary border-3 opacity-75">

```

--------------------------------

### Bootstrap Tooltip Markup Example (HTML)

Source: https://getbootstrap.com/docs/5.3/components/tooltips

Provides an example of the required HTML markup for a Bootstrap tooltip, including the `data-bs-toggle="tooltip"` and `data-bs-title` attributes. It also shows the generated markup of a tooltip by the plugin.

```html
<!-- HTML to write -->
<a href="#" data-bs-toggle="tooltip" data-bs-title="Some tooltip text!">Hover over me</a>

<!-- Generated markup by the plugin -->
<div class="tooltip bs-tooltip-auto" role="tooltip">
  <div class="tooltip-arrow"></div>
  <div class="tooltip-inner">
    Some tooltip text!
  </div>
</div>
```

--------------------------------

### Bootstrap 5.3 RTL Starter Template

Source: https://getbootstrap.com/docs/5.3/getting-started/rtl

A complete HTML starter template demonstrating the correct setup for Bootstrap 5.3 with RTL support. It includes the necessary `dir="rtl"` and `lang="ar"` attributes on the `<html>` tag, along with the RTL CSS file.

```html
<!doctype html>
<html lang="ar" dir="rtl">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.rtl.min.css" integrity="sha384-CfCrinSRH2IR6a4e6fy2q6ioOX7O6Mtm1L9vRvFZ1trBncWmMePhzvafv7oIcWiW" crossorigin="anonymous">

    <title>مرحبًا بالعالم!</title>
  </head>
  <body>
    <h1>مرحبًا بالعالم!</h1>

    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js" integrity="sha384-FKyoEForCGlyvwx9Hj09JcYn3nv7wiPVlz7YYwJrWVcXK/BmnVDxM+D2scQbITxI" crossorigin="anonymous"></script>

    <!-- Option 2: Separate Popper and Bootstrap JS -->
    <!--
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.min.js" integrity="sha384-G/EV+4j2dNv+tEPo3++6LCgdCROaejBqfUeNjuKAiuXbjrxilcCdDz6ZAVfHWe1Y" crossorigin="anonymous"></script>
    -->
  </body>
</html>

```

--------------------------------

### Basic Bootstrap Pagination Example

Source: https://getbootstrap.com/docs/5.3/components/pagination

Demonstrates a standard Bootstrap pagination component using an unordered list within a navigation element. It includes links for 'Previous', page numbers, and 'Next'. This structure is optimized for screen readers.

```html
<nav aria-label="Page navigation example">
  <ul class="pagination">
    <li class="page-item"><a class="page-link" href="#">Previous</a></li>
    <li class="page-item"><a class="page-link" href="#">1</a></li>
    <li class="page-item"><a class="page-link" href="#">2</a></li>
    <li class="page-item"><a class="page-link" href="#">3</a></li>
    <li class="page-item"><a class="page-link" href="#">Next</a></li>
  </ul>
</nav>
```

--------------------------------

### Bootstrap Nested Columns Example (md)

Source: https://getbootstrap.com/docs/5.3/examples/grid

Illustrates nesting columns within an existing column. This example creates two main columns (md-8 and md-4) with the first containing two nested, equal-width columns.

```html
.col-md-8
.col-md-6
.col-md-6
.col-md-4
```

--------------------------------

### Bootstrap Button Toggle HTML Examples

Source: https://getbootstrap.com/docs/5.3/components/buttons

Demonstrates how to use the `data-bs-toggle="button"` attribute to create toggleable buttons and links. Includes examples for various states like default, active, and disabled, and shows pre-toggling with `.active` class and `aria-pressed="true"` for accessibility.

```html
<p class="d-inline-flex gap-1">
  <button type="button" class="btn" data-bs-toggle="button">Toggle button</button>
  <button type="button" class="btn active" data-bs-toggle="button" aria-pressed="true">Active toggle button</button>
  <button type="button" class="btn" disabled data-bs-toggle="button">Disabled toggle button</button>
</p>
<p class="d-inline-flex gap-1">
  <button type="button" class="btn btn-primary" data-bs-toggle="button">Toggle button</button>
  <button type="button" class="btn btn-primary active" data-bs-toggle="button" aria-pressed="true">Active toggle button</button>
  <button type="button" class="btn btn-primary" disabled data-bs-toggle="button">Disabled toggle button</button>
</p>
<p class="d-inline-flex gap-1">
  <a href="#" class="btn" role="button" data-bs-toggle="button">Toggle link</a>
  <a href="#" class="btn active" role="button" data-bs-toggle="button" aria-pressed="true">Active toggle link</a>
  <a class="btn disabled" aria-disabled="true" role="button" data-bs-toggle="button">Disabled toggle link</a>
</p>
<p class="d-inline-flex gap-1">
  <a href="#" class="btn btn-primary" role="button" data-bs-toggle="button">Toggle link</a>
  <a href="#" class="btn btn-primary active" role="button" data-bs-toggle="button" aria-pressed="true">Active toggle link</a>
  <a class="btn btn-primary disabled" aria-disabled="true" role="button" data-bs-toggle="button">Disabled toggle link</a>
</p>
```

--------------------------------

### Overriding Global Box-Sizing in CSS

Source: https://getbootstrap.com/docs/5.3/getting-started/introduction

Bootstrap sets the global box-sizing to 'border-box' for easier CSS sizing. This snippet shows how to override it to 'content-box' for specific selectors, which might be necessary for third-party integrations.

```css
.selector-for-some-widget {
  box-sizing: content-box;
}

```

--------------------------------

### Bootstrap Navbar Example with Responsive Collapse

Source: https://getbootstrap.com/docs/5.3/components/navbar

A comprehensive example of a Bootstrap navbar that is responsive and collapses at the 'lg' breakpoint. It includes navigation links, a dropdown, a search form, and uses various utility classes for styling and spacing. Requires Bootstrap's JavaScript for collapse functionality.

```html
<nav class="navbar navbar-expand-lg bg-body-tertiary">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">Navbar</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="#">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#">Link</a>
        </li>
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Dropdown
          </a>
          <ul class="dropdown-menu">
            <li><a class="dropdown-item" href="#">Action</a></li>
            <li><a class="dropdown-item" href="#">Another action</a></li>
            <li><hr class="dropdown-divider"></li>
            <li><a class="dropdown-item" href="#">Something else here</a></li>
          </ul>
        </li>
        <li class="nav-item">
          <a class="nav-link disabled" aria-disabled="true">Disabled</a>
        </li>
      </ul>
      <form class="d-flex" role="search">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search"/>
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
    </div>
  </div>
</nav>
```

--------------------------------

### Bootstrap Live Toast Example with JavaScript

Source: https://getbootstrap.com/docs/5.3/components/toasts

This example demonstrates how to create a live, dismissible toast that can be triggered by a button click. It requires HTML for the button and toast container, along with JavaScript to initialize and show the toast using the Bootstrap Toast API.

```html
<button type="button" class="btn btn-primary" id="liveToastBtn">Show live toast</button>

<div class="toast-container position-fixed bottom-0 end-0 p-3">
  <div id="liveToast" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
    <div class="toast-header">
      <img src="..." class="rounded me-2" alt="...">
      <strong class="me-auto">Bootstrap</strong>
      <small>11 mins ago</small>
      <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast-body">
      Hello, world! This is a toast message.
    </div>
  </div>
</div>
```

```javascript
const toastTrigger = document.getElementById('liveToastBtn')
const toastLiveExample = document.getElementById('liveToast')

if (toastTrigger) {
  const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toastLiveExample)
  toastTrigger.addEventListener('click', () => {
    toastBootstrap.show()
  })
}
```

--------------------------------

### Bootstrap Button JavaScript Toggle All Example

Source: https://getbootstrap.com/docs/5.3/components/buttons

Provides a JavaScript example demonstrating how to toggle the state of all buttons on a page using `bootstrap.Button.getOrCreateInstance` and the `toggle` method. This is useful for applying a consistent action to multiple buttons.

```javascript
document.querySelectorAll('.btn').forEach(buttonElement => {
  const button = bootstrap.Button.getOrCreateInstance(buttonElement)
  button.toggle()
})
```

--------------------------------

### Bootstrap Dropstart Dropdowns (HTML)

Source: https://getbootstrap.com/docs/5.3/components/dropdowns

Illustrates how to create left-aligned dropdown menus using Bootstrap's `.dropstart` class. Provides examples for default and split button configurations.

```html
<div class="btn-group dropstart">
  <button type="button" class="btn btn-secondary dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false">
    Dropstart
  </button>
  <ul class="dropdown-menu">
    <!-- Dropdown menu links -->
  </ul>
</div>

<div class="btn-group dropstart">
  <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split" data-bs-toggle="dropdown" aria-expanded="false">
    <span class="visually-hidden">Toggle Dropstart</span>
  </button>
  <ul class="dropdown-menu">
    <!-- Dropdown menu links -->
  </ul>
  <button type="button" class="btn btn-secondary">
    Split dropstart
  </button>
</div>
```

--------------------------------

### HTML Inline Elements Example

Source: https://getbootstrap.com/docs/5.3/examples/blog

Illustrates the usage of common HTML inline semantic elements as styled by Bootstrap. This includes bold, italic, abbreviations, citations, deleted/inserted text, superscript, and subscript. These elements are core HTML and require no external libraries.

```html
<strong>To bold text</strong>, use <code>&lt;strong&gt;</code>.
<em>To italicize text</em>, use <code>&lt;em&gt;</code>.
Abbreviations, like HTML should use <code>&lt;abbr&gt;</code>, with an optional <code>title</code> attribute for the full phrase.
Citations, like — Mark Otto, should use <code>&lt;cite&gt;</code>.
<del>Deleted</del> text should use <code>&lt;del&gt;</code> and inserted text should use <code>&lt;ins&gt;</code>.
Superscript text uses <code>&lt;sup&gt;</code> and subscript text uses <code>&lt;sub&gt;</code>.
```

--------------------------------

### Bootstrap Basic Progress Bar Examples

Source: https://getbootstrap.com/docs/5.3/components/progress

Demonstrates the basic structure of Bootstrap progress bars with varying `aria-valuenow` attributes to represent different progress levels. These examples show how to create a wrapper with `role='progressbar'` and an inner `div` for the visual bar.

```html
<div class="progress" role="progressbar" aria-label="Basic example" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-bar" style="width: 0%"></div>
</div>
<div class="progress" role="progressbar" aria-label="Basic example" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-bar" style="width: 25%"></div>
</div>
<div class="progress" role="progressbar" aria-label="Basic example" aria-valuenow="50" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-bar" style="width: 50%"></div>
</div>
<div class="progress" role="progressbar" aria-label="Basic example" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-bar" style="width: 75%"></div>
</div>
<div class="progress" role="progressbar" aria-label="Basic example" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">
  <div class="progress-bar" style="width: 100%"></div>
</div>
```

--------------------------------

### Bootstrap Checkbox Examples (HTML)

Source: https://getbootstrap.com/docs/5.3/forms/checks-radios

Demonstrates the HTML structure for default and checked checkboxes using Bootstrap's `.form-check` and `.form-check-input` classes. These examples show how to create visually distinct checkboxes that are consistent across browsers.

```html
<div class="form-check">
  <input class="form-check-input" type="checkbox" value="" id="checkDefault">
  <label class="form-check-label" for="checkDefault">
    Default checkbox
  </label>
</div>
<div class="form-check">
  <input class="form-check-input" type="checkbox" value="" id="checkChecked" checked>
  <label class="form-check-label" for="checkChecked">
    Checked checkbox
  </label>
</div>
```

--------------------------------

### Get or Create Bootstrap Plugin Instance with JavaScript

Source: https://getbootstrap.com/docs/5.3/getting-started/javascript

This snippet demonstrates the `getOrCreateInstance` method for Bootstrap plugins. It retrieves an existing instance if available, or creates a new one if not. An optional configuration object can be passed as the second argument to configure the new instance.

```javascript
bootstrap.Popover.getOrCreateInstance(myPopoverEl, configObject)
```

--------------------------------

### Bootstrap Custom File Input Examples in Input Groups

Source: https://getbootstrap.com/docs/5.3/forms/input-group

Illustrates how to incorporate file input elements within Bootstrap's input groups. These examples showcase different arrangements for labels and buttons alongside the file upload control.

```html
<div class="input-group mb-3">
  <label class="input-group-text" for="inputGroupFile01">Upload</label>
  <input type="file" class="form-control" id="inputGroupFile01">
</div>

<div class="input-group mb-3">
  <input type="file" class="form-control" id="inputGroupFile02">
  <label class="input-group-text" for="inputGroupFile02">Upload</label>
</div>

<div class="input-group mb-3">
  <button class="btn btn-outline-secondary" type="button" id="inputGroupFileAddon03">Button</button>
  <input type="file" class="form-control" id="inputGroupFile03" aria-describedby="inputGroupFileAddon03" aria-label="Upload">
</div>

<div class="input-group">
  <input type="file" class="form-control" id="inputGroupFile04" aria-describedby="inputGroupFileAddon04" aria-label="Upload">
  <button class="btn btn-outline-secondary" type="button" id="inputGroupFileAddon04">Button</button>
</div>
```

--------------------------------

### Configure HTML Entry Point for Parcel

Source: https://getbootstrap.com/docs/5.3/getting-started/parcel

Defines the main HTML file for Parcel to render. This file includes links to the SCSS stylesheet and the main JavaScript module, setting up the basic structure for the web page and integrating Bootstrap's container and button classes.

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap w/ Parcel</title>
    <link rel="stylesheet" href="scss/styles.scss">
    <script type="module" src="js/main.js"></script>
  </head>
  <body>
    <div class="container py-4 px-3 mx-auto">
      <h1>Hello, Bootstrap and Parcel!</h1>
      <button class="btn btn-primary">Primary button</button>
    </div>
  </body>
</html>

```

--------------------------------

### Override Sass Variable and Recompile (Bash)

Source: https://getbootstrap.com/docs/5.3/customize/options

This command demonstrates how to override a Bootstrap Sass variable and recompile the project. It assumes you have npm installed and are in the project's root directory. The `npm run test` command is used here as an example; your project might use a different script for compilation.

```bash
npm run test
```

--------------------------------

### Bootstrap 5.3 Grid Mixin Example (SCSS)

Source: https://getbootstrap.com/docs/5.3/layout/grid

Demonstrates how to create a two-column layout with a gap using Bootstrap's grid mixins. It defines container, row, and column styles, including responsive adjustments for different screen sizes. This example relies on the core Bootstrap Sass framework.

```scss
.example-container {
  @include make-container();
  // Make sure to define this width after the mixin to override
  // `width: 100%` generated by `make-container()`
  width: 800px;
}

.example-row {
  @include make-row();
}

.example-content-main {
  @include make-col-ready();

  @include media-breakpoint-up(sm) {
    @include make-col(6);
  }
  @include media-breakpoint-up(lg) {
    @include make-col(8);
  }
}

.example-content-secondary {
  @include make-col-ready();

  @include media-breakpoint-up(sm) {
    @include make-col(6);
  }
  @include media-breakpoint-up(lg) {
    @include make-col(4);
  }
}

```
