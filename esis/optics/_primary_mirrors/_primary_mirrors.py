import abc
import dataclasses
import numpy as np
import astropy.units as u
import named_arrays as na
import optika

__all__ = [
    "AbstractPrimaryMirror",
    "PrimaryMirror",
]


@dataclasses.dataclass(eq=False, repr=False)
class AbstractPrimaryMirror(
    optika.mixins.Printable,
    optika.mixins.Rollable,
    optika.mixins.Yawable,
    optika.mixins.Pitchable,
    optika.mixins.Translatable,
):
    """
    An interface describing the primary mirror of the instrument.
    """

    @property
    @abc.abstractmethod
    def sag(self) -> None | optika.sags.AbstractSag:
        """
        The sag function of this primary mirror.
        """

    @property
    @abc.abstractmethod
    def num_folds(self) -> u.Quantity | na.AbstractScalar:
        """
        The order of the rotational symmetry of the optical system.
        This is also the number of sides of the regular polygonal aperture.
        """

    @property
    @abc.abstractmethod
    def width_clear(self) -> u.Quantity | na.AbstractScalar:
        """
        The width of the clear aperture from edge to edge.
        """

    @property
    def radius_clear(self) -> u.Quantity | na.AbstractScalar:
        """
        The clear radius of the aperture from center to vertex.
        """
        halfwidth_clear = self.width_clear / 2
        num_sides = self.num_folds
        if (num_sides % 2) != 0:  # pragma: nocover
            raise ValueError("odd numbers of sides not supported")
        result = halfwidth_clear / np.cos(360 * u.deg / num_sides / 2)
        return result

    @property
    @abc.abstractmethod
    def width_border(self) -> u.Quantity | na.AbstractScalar:
        """
        The width of the border around the clear aperture.
        """

    @property
    def radius_mechanical(self) -> u.Quantity | na.AbstractScalar:
        """
        The radius of the mechanical aperture from center to vertex.
        """
        halfwidth_clear = self.width_clear / 2
        width_border = self.width_border
        halfwidth = halfwidth_clear + width_border
        num_sides = self.num_folds
        if (num_sides % 2) != 0:  # pragma: nocover
            raise ValueError("odd numbers of sides not supported")
        result = halfwidth / np.cos(360 * u.deg / num_sides / 2)
        return result

    @property
    @abc.abstractmethod
    def material(self) -> None | optika.materials.AbstractMaterial:
        """
        The optics material composing this object.
        """

    @property
    def surface(self) -> optika.surfaces.Surface:
        """
        Represent this object as an :mod:`optika` surface.
        """
        return optika.surfaces.Surface(
            name="primary",
            sag=self.sag,
            material=self.material,
            aperture=optika.apertures.RegularPolygonalAperture(
                radius=self.radius_clear,
                num_vertices=self.num_folds,
            ),
            aperture_mechanical=optika.apertures.RegularPolygonalAperture(
                radius=self.radius_mechanical,
                num_vertices=self.num_folds,
            ),
            transformation=self.transformation,
        )


@dataclasses.dataclass(eq=False, repr=False)
class PrimaryMirror(
    AbstractPrimaryMirror,
):
    """
    A model of the primary mirror of the instrument.

    This mirror collects light from the Sun and focuses it onto the field stop.
    """

    sag: None | optika.sags.AbstractSag = None
    """
    The sag function of this primary mirror.
    """

    num_folds: int = 0
    """
    The order of the rotational symmetry of the optical system.
    This is also the number of sides of the regular polygonal aperture.
    """

    width_clear: u.Quantity | na.AbstractScalar = 0 * u.mm
    """
    The width of the clear aperture from edge to edge.
    """

    width_border: u.Quantity | na.AbstractScalar = 0 * u.mm
    """
    The width of the border around the clear aperture.
    """

    material: None | optika.materials.AbstractMaterial = None
    """
    The optical material composing this object.
    """

    translation: u.Quantity | na.AbstractCartesian3dVectorArray = 0 * u.mm
    """
    A transformation which can arbitrarily translate this object.
    """

    pitch: u.Quantity | na.AbstractScalar = 0 * u.deg
    """
    The pitch angle of this object.
    """

    yaw: u.Quantity | na.AbstractScalar = 0 * u.deg
    """
    The yaw angle of this object.
    """

    roll: u.Quantity | na.AbstractScalar = 0 * u.deg
    """
    The roll angle of this object
    """
