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

Documentation is forthcoming.

## Contributing

Pull requests are welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.