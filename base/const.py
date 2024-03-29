ADMIN = 1
USER = 2
USER_TYPE_CHOICES = (
    (ADMIN, 'admin'),
    (USER, 'user'),
)

DEACTIVE = 0
ACTIVE = 1
STATUS_CHOICES = (
    (ACTIVE, 'Active'),
    (DEACTIVE, 'Deactive'),
)

MALE = 'M'
FEMALE = 'F'
GENDER_TYPE = (
    (MALE, 'Male'),
    (FEMALE, 'Female'),
)

BILLING = 'billing'
SHIPPING = 'shipping'
ADDRESS_TYPE = (
    (BILLING, 'Billing'),
    (SHIPPING, 'Shipping'),
)

CHECKED = 0
NOT_CHECKED = 1
READ_STATUS_CHOICES = (
    (CHECKED, 'Checked'),
    (NOT_CHECKED, 'Not Checked'),
)

CONTACT_US = 0
POST_REQUIREMENT = 1
CONTACT_TYPE_CHOICES = (
    (CONTACT_US, 'Contact us'),
    (POST_REQUIREMENT, 'Post Requirement'),
)

RETURN_POLICY = 0
FAQ = 1
DETAILS_TYPE_CHOICES = (
    (RETURN_POLICY, 'Return Policy'),
    (FAQ, 'FAQ'),
)

FLAT = 0
PERCENTAGE = 1
OFFER_TYPE_CHOICES = (
    (FLAT, 'Flat'),
    (PERCENTAGE, '%'),
)

PENDING = 0
PROCESSING = 1
PAID = 2
CANCELLED = 3
FAILED = 4
PAYMENT_STATUS_CHOICES = (
    (PENDING, 'Pending'),
    (PROCESSING, 'Processing'),
    (PAID, 'Paid'),
    (CANCELLED, 'Cancelled'),
    (FAILED, 'Failed'),
)

TRACK_ORDER_PENDING = 0
TRACK_ORDER_PROCESSING = 1
TRACK_ORDER_SHIPPED = 2
TRACK_ORDER_CANCELLED = 3
TRACK_ORDER_RETURNED = 4
TRACK_ORDER_STATUS_CHOICES = (
    (TRACK_ORDER_PENDING, 'Pending'),
    (TRACK_ORDER_PROCESSING, 'Processing'),
    (TRACK_ORDER_SHIPPED, 'Shipped'),
    (TRACK_ORDER_CANCELLED, 'Cancelled'),
    (TRACK_ORDER_RETURNED, 'Returned'),
)

POLISH_SHAPE_ROUND = 0
POLISH_SHAPE_PRINCESS = 1
POLISH_SHAPE_CUSHION = 2
POLISH_SHAPE_OVAL = 3
POLISH_SHAPE_EMERALD = 4
POLISH_SHAPE_HEART = 5
POLISH_SHAPE_PEAR = 6
POLISH_SHAPE_MARQUISE = 7
POLISH_SHAPE_ASSCHER = 8
POLISH_SHAPE_RADIANT = 9
POLISH_SHAPE_CHOICES = (
    (POLISH_SHAPE_ROUND, 'Round'),
    (POLISH_SHAPE_PRINCESS, 'Princess'),
    (POLISH_SHAPE_CUSHION, 'Cushion'),
    (POLISH_SHAPE_OVAL, 'Oval'),
    (POLISH_SHAPE_EMERALD, 'Emerald'),
    (POLISH_SHAPE_HEART, 'Heart'),
    (POLISH_SHAPE_PEAR, 'Pear'),
    (POLISH_SHAPE_MARQUISE, 'Marquise'),
    (POLISH_SHAPE_ASSCHER, 'Asscher'),
    (POLISH_SHAPE_RADIANT, 'Radiant'),
)

POLISH_CUT_POOR = 0
POLISH_CUT_FAIR = 1
POLISH_CUT_GOOD = 2
POLISH_CUT_VERY_GOOD = 3
POLISH_CUT_EXCELLENT = 4
POLISH_CUT_CHOICES = (
    (POLISH_CUT_POOR, 'Poor'),
    (POLISH_CUT_FAIR, 'Fair'),
    (POLISH_CUT_GOOD, 'Good'),
    (POLISH_CUT_VERY_GOOD, 'Very Good'),
    (POLISH_CUT_EXCELLENT, 'Excellent'),
)

POLISH_PURITY_FL = 0
POLISH_PURITY_IF = 1
POLISH_PURITY_VVS1 = 2
POLISH_PURITY_VVS2 = 3
POLISH_PURITY_VS1 = 4
POLISH_PURITY_VS2 = 5
POLISH_PURITY_SI1 = 6
POLISH_PURITY_SI2 = 7
POLISH_PURITY_SI3 = 8
POLISH_PURITY_I1 = 9
POLISH_PURITY_CHOICES = (
    (POLISH_PURITY_FL, 'FL'),
    (POLISH_PURITY_IF, 'IF'),
    (POLISH_PURITY_VVS1, 'VVS1'),
    (POLISH_PURITY_VVS2, 'VVS2'),
    (POLISH_PURITY_VS1, 'VS1'),
    (POLISH_PURITY_VS2, 'VS2'),
    (POLISH_PURITY_SI1, 'SI1'),
    (POLISH_PURITY_SI2, 'SI2'),
    (POLISH_PURITY_SI3, 'SI3'),
    (POLISH_PURITY_I1, 'I1'),
)

POLISH_COLOR_D = 0
POLISH_COLOR_E = 1
POLISH_COLOR_F = 2
POLISH_COLOR_G = 3
POLISH_COLOR_H = 4
POLISH_COLOR_I = 5
POLISH_COLOR_J = 6
POLISH_COLOR_K = 7
POLISH_COLOR_L = 8
POLISH_COLOR_M = 9
POLISH_COLOR_N = 10
POLISH_COLOR_CHOICES = (
    (POLISH_COLOR_D, 'D'),
    (POLISH_COLOR_E, 'E'),
    (POLISH_COLOR_F, 'F'),
    (POLISH_COLOR_G, 'G'),
    (POLISH_COLOR_H, 'H'),
    (POLISH_COLOR_I, 'I'),
    (POLISH_COLOR_J, 'J'),
    (POLISH_COLOR_K, 'K'),
    (POLISH_COLOR_L, 'L'),
    (POLISH_COLOR_M, 'M'),
    (POLISH_COLOR_N, 'N'),
)

POLISH_FLUORESCENCE_NONE = 0
POLISH_FLUORESCENCE_FAINT = 1
POLISH_FLUORESCENCE_MEDIUM = 2
POLISH_FLUORESCENCE_STRONG = 3
POLISH_FLUORESCENCE_VERY_STRONG = 4
POLISH_FLUORESCENCE_CHOICES = (
    (POLISH_FLUORESCENCE_NONE, 'None'),
    (POLISH_FLUORESCENCE_FAINT, 'Faint'),
    (POLISH_FLUORESCENCE_MEDIUM, 'Medium'),
    (POLISH_FLUORESCENCE_STRONG, 'Strong'),
    (POLISH_FLUORESCENCE_VERY_STRONG, 'Very Strong'),
)
