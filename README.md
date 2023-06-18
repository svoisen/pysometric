# Pysometric

Pysometric is a simple Python library for creating isometric 3D line art that can be rendered to SVG, typically for use with pen plotters. 

It is currently intended to be used in conjunction with the [vsketch](https://github.com/abey79/vsketch/) generative toolkit (though this dependency may be removed in the future).

<img src="https://i.imgur.com/247GGvX.png" alt="cube, pyramid and hexagonal prism" width="372">

## Features

* Renders 2D rectangles and polygons in 3D isometric projection
* Allows creation of complex 3D shapes from groups of polygons (e.g. boxes, pyramids, prisms)
* Supports textures (e.g. hatch and solid fills) on any polygon
* Automatically occludes lines (hidden line removal) based on scene z-order

# Getting Started

## Required dependencies

`Pysometric` currently requires [vsketch](https://github.com/abey79/vsketch) for rendering. You will need to install `vsketch` before using this library. 

## Installation

To get started with Pysometric, clone the repository and install it using `pip`:

```bash
$ git clone https://github.com/svoisen/pysometric.git
$ cd pysometric
$ pip install .
```

## Examples

Once the library is installed you can create a simple isometric scene using `pysometric` inside a `vsketch` sketch. For example, in the `draw` method of your sketch:

```python
# Create a frame for the scene that is the same size as the vsketch page
frame = shapely.box(0, 0, vsk.width, vsk.height)

# Create a Scene with a single 3D box at the origin and
# a grid pitch size of 100 CSS pixels
box = Box((0, 0, 0))
scene = Scene(frame, 100, [box])

# Render the scene to ths ketch
scene.render(vsk)
```

More examples may be found in the `examples` directory.

# Running tests

This project uses pytest. Run tests by executing the following in the root directory of the repository:

```bash
$ pytest
```

# Documentation

## Using Pysometric

`Pysometric` is intended for the creation of static isometric 3D scenes as line art. It is not a true 3D system, nor does it support animation. As such, it is intentionally limited by the following constraints:

1. `Pysometric`'s API is immutable. Setup your scene once, then render it. That's it. Because it does not support animation, scenes, shapes and volumes in `pysometric` cannot be modified after their initial creation.
2. `Pysometric` has no concept of light sources. Shadows can be emulated using hatching or fill textures on polygons, but they cannot be generated automatically for a shape or entire scene based on lighting.

## API

### Scene

A `Scene` defines an isometric 3D scene that can be rendered to 2D line art. All shapes to be rendered by `pysometric` must be part of a scene. When creating a `Scene` you must specify:

* `grid_pitch`: The size of single grid coordinate unit for the 3D scene, which controls the overall scale of the scene.
* `frame`: A scene has a `frame` that defines its rendering boundaries, and can be any `shapely` polygon.
* `children`: A list of all of the child `Renderable`s in the scene. The order of this list defines the order in which the objects are rendered. Items in the list are rendered from first to last, meaning that items with lower indices will occlude items with higher indices, irrespective of their position in 3D space.

The `Scene` has a `render` method that accepts a `Vsketch` instance as a parameter and outputs the scene to the given sketch.

### Axes, Planes and Coordinates

All 3D coordinates should be specified as `Vector3` objects defining (x, y, z) positions. Axes in `pysometric` are as follows:

* x-axis: The axis oriented visually left to right (at an upward diagonal)
* y-axis: The axis oriented visually from back to front (at a downward diagonal)
* z-axis: The vertical axis running from bottom to top

### Renderable

The base class for any object that can be added to a Scene. All `Renderables` have a `compile` method which is used during rendering to compile the object into a `RenderableGeometry.`

### RenderableGeometry

A `RenderableGeometry` is the output of the `compile` method for a `Renderable,` and includes information necessary for rendering the object in 2D, such as its 2D geometry, stroke thickness and stroke color (layer).

### Polygon

A `Polygon` defines a general polygon shape. It is a subclass of `Renderable`.

#### Initialization

A `Polygon` is initialized with:

* `vertices`: A list of `Vector3` objects defining the vertices of the polygon. The vertices should be specified in clockwise or counter-clockwise order. 
* `textures`: Optional list of `Texture` objects to apply to the polygon.
* `rotations`: Optional list of `Rotation` objects to rotate the polygon.
* `layer`: The layer for the polygon. Default is 1.

#### Example

The following example creates a square polygon with vertices at (0, 0, 0), (10, 0, 0), (10, 10, 0) and (0, 10, 0):

```python
polygon = Polygon([
    (0, 0, 0), 
    (10, 0, 0),
    (10, 10, 0),
    (0, 10, 0)
])
```

### RegularPolygon

The `RegularPolygon` defines a symmetrical polygon with a specific number of sides. It is a subclass of `Polygon` and `Renderable`.

#### Initialization

A `RegularPolygon` is initialized with:

* `origin`: The (x, y, z) coordinates of the center of the polygon defined as a `Vector3`.
* `num_vertices`: The number of vertices/sides for the polygon. Must be 3 or greater.
* `radius`: The radius/distance from the center to each vertex.
* `orientation`: The plane in which the polygon lies. Must be one of Plane.XY, Plane.XZ or Plane.YZ.
* `textures`: Optional list of `Texture` objects to apply to the polygon.
* `rotations`: Optional list of `Rotation` objects to rotate the polygon.
* `layer`: The layer for the polygon. Default is 1.

#### Example:

The following example creates a hexagon with radius 10 at the origin on the plane defined by the X and Y axes.

```python
polygon = RegularPolygon((0, 0, 0), 6, 10, Plane.XY)
```

### Rectangle

A `Rectangle` defines a rectangular polygon in 3D space. 

By default, rectangles have an orientation parallel to one of the 3 possible planes defined in the `Plane` enumeration.

#### Initialization

A `Rectangle` is initialized with:

* `origin`: The (x, y, z) coordinates of the center of the rectangle defined as a `Vector3`.
* `width`: The width of the rectangle.
* `height`: The height of the rectangle. 
* `orientation`: The plane in which the rectangle lies. Must be one of `Plane.XY`, `Plane.XZ` or `Plane.YZ`.
* `textures`: Optional list of `Texture` objects to apply to the rectangle.
* `rotations`: Optional list of `Rotation` objects to rotate the rectangle.
* `layer`: The layer for the rectangle. Default is 1.

#### Example

The following example creates a rectangle with width 10 and height 5 centered at the origin on the XZ plane:

```python
rectangle = Rectangle((0, 0, 0), 10, 5, Plane.XZ)
```

### Group

A `Group` defines a collection of `Renderable` objects that should be treated as a single object. Groups allow you to organize complex shapes in your scene by combining multiple polygons and volumes.

#### Initialization

A `Group` is initialized with:

* `children`: A list of `Renderable` objects (e.g. `Polygon`, `Rectangle`, `Box`, `Prism`) that make up the group.

#### Example

The following example creates a `Group` that renders as a cube, defined by 6 `Rectangle` objects (one for each side of the cube):

```python
cube = Group([
    Rectangle((0, 0, 0), 10, 10, Plane.XY),  # Top face
    Rectangle((0, 0, -10), 10, 10, Plane.XY), # Bottom face
    Rectangle((0, -10, 0), 10, 10, Plane.YZ), # Front face
    Rectangle((0, 10, 0), 10, 10, Plane.YZ),  # Back face
    Rectangle((-10, 0, 0), 10, 10, Plane.XZ), # Left face
    Rectangle((10, 0, 0), 10, 10, Plane.XZ)   # Right face
])
```

### Box

### Prism

### Texture

### HatchTexture

### FillTexture

# Contributing

Pull requests are welcome.

# License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.