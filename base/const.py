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
POST_REQUIRMENT = 1
CONTACT_TYPE_CHOICES = (
    (CONTACT_US, 'Contact us'),
    (POST_REQUIRMENT, 'Post Requirment'),
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