from dependency_injector import containers, providers

# Import các thành phần của Product
from src.services.product_service import ProductService
from src.infrastructure.repositories.product_repository import SqlProductRepository
from src.api.controllers.product_controller import ProductController

# Import các thành phần mới (Auth, Order, User, Customer)
from src.services.auth_service import AuthService
from src.services.order_service import OrderService
from src.infrastructure.repositories.user_repository import SqlUserRepository
from src.infrastructure.repositories.order_repository import SqlOrderRepository
from src.api.controllers.auth_controller import AuthController
from src.api.controllers.customer_controller import CustomerController

class AppContainer(containers.DeclarativeContainer):

    # === Repositories ===
    product_repository = providers.Singleton(SqlProductRepository)
    user_repository = providers.Singleton(SqlUserRepository)
    order_repository = providers.Singleton(SqlOrderRepository)

    # === Services ===
    product_service = providers.Factory(
        ProductService,
        product_repo=product_repository
    )

    auth_service = providers.Factory(
        AuthService,
        user_repo=user_repository
    )

    order_service = providers.Factory(
        OrderService,
        order_repo=order_repository,
        product_repo=product_repository,
        user_repo=user_repository
    )

    # === Controllers ===
    product_controller = providers.Factory(
        ProductController,
        product_service=product_service
    )

    auth_controller = providers.Factory(
        AuthController,
        auth_service=auth_service
    )

    customer_controller = providers.Factory(
        CustomerController,
        order_service=order_service,
        product_service=product_service
    )
