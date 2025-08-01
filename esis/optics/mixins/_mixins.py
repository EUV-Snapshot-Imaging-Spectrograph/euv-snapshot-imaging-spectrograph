import abc
import dataclasses
import astropy.units as u
import named_arrays as na
import optika

__all__ = [
    "CylindricallyTransformable",
]


@dataclasses.dataclass(eq=False, repr=False)
class CylindricallyTransformable(
    optika.mixins.Transformable,
):
    """
    A mixin class which can apply a cylindrical transformation to subclasses.
    """

    @property
    @abc.abstractmethod
    def distance_radial(self) -> u.Quantity | na.AbstractScalar:
        """
        The distance of this object from the axis of symmetry.
        """

    @property
    @abc.abstractmethod
    def azimuth(self) -> u.Quantity | na.AbstractScalar:
        """
        The angle of rotation about the axis of symmetry.
        """

    @property
    def transformation(self) -> na.transformations.AbstractTransformation:
        t = na.transformations.TransformationList(
            [
                na.transformations.Cartesian3dTranslation(x=self.distance_radial),
                na.transformations.Cartesian3dRotationZ(self.azimuth),
            ]
        )
        return super().transformation @ t
