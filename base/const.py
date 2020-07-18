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
