from django.db import models
from django.core.validators import MinValueValidator # Dùng để chặn số âm
from decimal import Decimal
# Create your models here.
class Product(models.Model):
    # 1. Tên sản phẩm
    name = models.CharField(max_length=200, null=False, blank=False)
    # 2. Danh mục (Category)
    category = models.CharField(max_length=100, null=False, blank=False)
    # 3. Đơn giá (Price)
    price = models.DecimalField(
        max_digits=15,
        decimal_places=0,
        validators=[MinValueValidator(Decimal('0.00'))])  # Không cho nhập giá âm
    # 4. Số lượng tồn kho (Quantity)
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],  # Không cho nhập số lượng âm
        null=False,
        blank=False
    )
    # 5. Hình ảnh sản phẩm (Image)
    image = models.ImageField(
        upload_to='products/',
        null=True,
        blank=True,
    )
    # 6. Mô tả (Description)
    description = models.TextField(
        null=True,
        blank=True,
    )
    # 7. Các trường quản lý thời gian (Tự động)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

    # --- LOGIC TÍNH TOÁN ---

    #Hàm này tự động tính toán tổng giá trị sản phẩm tồn kho mà không cần lưu vào database
    @property
    def total_value(self):
        if self.price and self.quantity:
            total = self.price * self.quantity
            return total
        return 0

    # Hàm kiểm tra trạng thái kho để hiện màu sắc cảnh báo
    @property
    def stock_status(self):
        if self.quantity == 0:
            return 'out_of_stock'  # Hết hàng
        elif self.quantity < 10:
            return 'low_stock'  # Sắp hết
        return 'in_stock'  # Còn hàng
