# Pysometric

Pysometric is a simple Python library for creating isometric drawings that can be rendered to SVG, typically for use with pen plotters. It is currently intended to be used in conjunction with the [vsketch](https://github.com/abey79/vsketch/) generative toolkit.

## Features

* Renders 2D rectangles and polygons in 3D isometric projection
* Allows creationg of complex 3D shapes from groups of polygons (e.g. boxes, pyramids)
* Supports textures (e.g. hatch and solid fills) on any polygon
* Automatically occludes lines (hidden line removal) based on z-order

## Getting Started

### Required dependencies

Currently requires [vsketch](https://github.com/abey79/vsketch) for rendering. (This dependency may be removed in the future for more versatility.)

### Installation

To get started with Pysometric, install it using pip:

```bash
$ pip install pysometric
```

### Examples

Once the library is installed you can create a simple isometric scene using `pysometric` inside a `vsketch` sketch. For example, in the `draw` method of your sketch:

```python
# Create a frame for the scene that is the same size as the vsketch page
frame = shapely.box(0, 0, vsk.width, vsk.height)

# Create a Scene with a single 3D box at the origin 
box = Box((0, 0, 0))
scene = Scene(frame, 1, [box])

# Render the scene to ths ketch
scene.render(vsk)
```

More examples may be found in the `examples` directory.

### Running tests

This project uses pytest. Run tests by executing the following in the root directory of the repository:

```bash
$ pytest
```

## Documentation

### Using Pysometric

`Pysometric` is intended for the creation of static isometric 3D scenes as line art. It is not a true 3D system, and has no support for animation. As such, it is intentionally limited by the following constraints:

1. `Pysometric`'s API is intentionally immutable. Setup your scene once, then render it. Because it does not support animation, scenes, shapes and volumes in `pysometric` cannot be modified after their initial creation.
2. `Pysometric` has no concept of light sources. Shadows can be emulated using hatching or fill textures on polygons, but they cannot be generated automatically for a shape or entire scene based on lighting.

### API

#### Scene

A `Scene` defines an isometric 3D scene that can be rendered to 2D line art. All shapes to be rendered by `pysometric` must be part of a scene. When creating a `Scene` you must specify:

* `grid_pitch`: The size of single grid coordinate unit for the 3D scene, which controls the overall scale of the scene.
* `frame`: A scene has a `frame` that defines its rendering boundaries, and can be any `shapely` polygon.
* `children`: A list of all of the child `Renderable`s in the scene. The order of this list defines the order in which the objects are rendered. Items in the list are rendered from first to last, meaning that items with lower indices will occlude items with higher indices, irrespective of their position in 3D space.

The `Scene` has a `render` method that accepts a `Vsketch` instance as a parameter and outputs the scene to the given sketch.

#### Renderable

The base class for any object that can be added to a Scene. All `Renderables` have a `compile` method which is used during rendering to compile the object into a `RenderableGeometry.`

#### RenderableGeometry

A `RenderableGeometry` is the output of the `compile` method for a `Renderable,` and includes information necessary for rendering the object in 2D, such as its 2D geometry, stroke thickness and stroke color (layer).

#### Polygon

#### RegularPolygon

The `RegularPolygon` defines a symmetrical polygon of arbitrary sides. It is a subclass of Polygon and Renderable.

Initialization

A `RegularPolygon` is initialized with:

* `origin`: The (x, y, z) coordinates of the center of the polygon defined as a `Vector3`.
* num_vertices: The number of vertices/sides for the polygon. Must be 3 or greater.
* radius: The radius/distance from the center to each vertex.
* orientation: The plane in which the polygon lies. Must be one of Plane.XY, Plane.XZ or Plane.YZ.
* textures: Optional list of Texture objects to apply to the polygon.
* rotations: Optional list of Rotation objects to rotate the polygon.
* layer: The layer for the polygon. Default is 1.

#### Rectangle

#### Group

#### Box

#### Prism

#### Texture

## Contributing

Pull requests are welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.