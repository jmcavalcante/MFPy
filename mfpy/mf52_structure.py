from dataclasses import dataclass, field
from typing import Any

# Definindo todas as dataclasses
@dataclass
class MDIHeader:
    FILE_TYPE: Any = None
    FILE_VERSION: Any = None
    FILE_FORMAT: Any = None

@dataclass
class Units:
    LENGTH: Any = None
    FORCE: Any = None
    ANGLE: Any = None
    MASS: Any = None
    TIME: Any = None

@dataclass
class Model:
    FITTYP: Any = None
    USE_MODE: Any = None
    VXLOW: Any = None
    LONGVL: Any = None
    TYRESIDE: Any = None

@dataclass
class Dimension:
    UNLOADED_RADIUS: Any = None
    WIDTH: Any = None
    ASPECT_RATIO: Any = None
    RIM_RADIUS: Any = None
    RIM_WIDTH: Any = None

@dataclass
class Vertical:
    FNOMIN: Any = None
    VERTICAL_STIFFNESS: Any = None
    VERTICAL_DAMPING: Any = None
    BREFF: Any = None
    DREFF: Any = None
    FREFF: Any = None

@dataclass
class LongSlipRange:
    KPUMIN: Any = None
    KPUMAX: Any = None

@dataclass
class SlipAngleRange:
    ALPMIN: Any = None
    ALPMAX: Any = None

@dataclass
class InclinationAngleRange:
    CAMMIN: Any = None
    CAMMAX: Any = None

@dataclass
class VerticalForceRange:
    FZMIN: Any = None
    FZMAX: Any = None

@dataclass
class ScalingCoefficients:
    LFZO: Any = None
    LCX: Any = None
    LMUX: Any = None
    LEX: Any = None
    LKX: Any = None
    LHX: Any = None
    LVX: Any = None
    LGAX: Any = None
    LCY: Any = None
    LMUY: Any = None
    LEY: Any = None
    LKY: Any = None
    LHY: Any = None
    LVY: Any = None
    LGAY: Any = None
    LTR: Any = None
    LRES: Any = None
    LGAZ: Any = None
    LMX: Any = None
    LVMX: Any = None
    LMY: Any = None
    LXAL: Any = None
    LYKA: Any = None
    LVYKA: Any = None
    LS: Any = None

@dataclass
class LongitudinalCoefficients:
    PCX1: Any = None
    PDX1: Any = None
    PDX2: Any = None
    PDX3: Any = None
    PEX1: Any = None
    PEX2: Any = None
    PEX3: Any = None
    PEX4: Any = None
    PKX1: Any = None
    PKX2: Any = None
    PKX3: Any = None
    PHX1: Any = None
    PHX2: Any = None
    PVX1: Any = None
    PVX2: Any = None
    RBX1: Any = None
    RBX2: Any = None
    RCX1: Any = None
    REX1: Any = None
    REX2: Any = None
    RHX1: Any = None

@dataclass
class LateralCoefficients:
    PCY1: Any = None
    PDY1: Any = None
    PDY2: Any = None
    PDY3: Any = None
    PEY1: Any = None
    PEY2: Any = None
    PEY3: Any = None
    PEY4: Any = None
    PKY1: Any = None
    PKY2: Any = None
    PKY3: Any = None
    PHY1: Any = None
    PHY2: Any = None
    PHY3: Any = None
    PVY1: Any = None
    PVY2: Any = None
    PVY3: Any = None
    PVY4: Any = None
    RBY1: Any = None
    RBY2: Any = None
    RBY3: Any = None
    RCY1: Any = None
    REY1: Any = None
    REY2: Any = None
    RHY1: Any = None
    RHY2: Any = None
    RVY1: Any = None
    RVY2: Any = None
    RVY3: Any = None
    RVY4: Any = None
    RVY5: Any = None
    RVY6: Any = None

@dataclass
class AligningCoefficients:
    QBZ1: Any = None
    QBZ2: Any = None
    QBZ3: Any = None
    QBZ4: Any = None
    QBZ5: Any = None
    QBZ9: Any = None
    QBZ10: Any = None
    QCZ1: Any = None
    QDZ1: Any = None
    QDZ2: Any = None
    QDZ3: Any = None
    QDZ4: Any = None
    QDZ6: Any = None
    QDZ7: Any = None
    QDZ8: Any = None
    QDZ9: Any = None
    QEZ1: Any = None
    QEZ2: Any = None
    QEZ3: Any = None
    QEZ4: Any = None
    QEZ5: Any = None
    QHZ1: Any = None
    QHZ2: Any = None
    QHZ3: Any = None
    QHZ4: Any = None
    SSZ1: Any = None
    SSZ2: Any = None
    SSZ3: Any = None
    SSZ4: Any = None

@dataclass
class RollingCoefficients:
    QSY1: Any = None
    QSY2: Any = None
    QSY3: Any = None
    QSY4: Any = None

@dataclass
class OverturningCoefficients:
    QSX1: Any = None
    QSX2: Any = None
    QSX3: Any = None

@dataclass
class MF52:
    MDI_HEADER: MDIHeader = field(default_factory=MDIHeader)
    UNITS: Units = field(default_factory=Units)
    MODEL: Model = field(default_factory=Model)
    DIMENSION: Dimension = field(default_factory=Dimension)
    VERTICAL: Vertical = field(default_factory=Vertical)
    LONG_SLIP_RANGE: LongSlipRange = field(default_factory=LongSlipRange)
    SLIP_ANGLE_RANGE: SlipAngleRange = field(default_factory=SlipAngleRange)
    INCLINATION_ANGLE_RANGE: InclinationAngleRange = field(default_factory=InclinationAngleRange)
    VERTICAL_FORCE_RANGE: VerticalForceRange = field(default_factory=VerticalForceRange)
    SCALING_COEFFICIENTS: ScalingCoefficients = field(default_factory=ScalingCoefficients)
    LONGITUDINAL_COEFFICIENTS: LongitudinalCoefficients = field(default_factory=LongitudinalCoefficients)
    LATERAL_COEFFICIENTS: LateralCoefficients = field(default_factory=LateralCoefficients)
    OVERTURNING_COEFFICIENTS: OverturningCoefficients = field(default_factory=OverturningCoefficients)
    ROLLING_COEFFICIENTS: RollingCoefficients = field(default_factory=RollingCoefficients)
    ALIGNING_COEFFICIENTS: AligningCoefficients = field(default_factory=AligningCoefficients)

mf_52 = MF52()