"""Example usage of UserRepository with SQLModel.

This module demonstrates how to use the UserRepository in your application.
"""
from src.core.database.session import get_session
from src.core.repositories.user_repository import UserRepository
from src.domain.users.models import User, UserPermission


def example_user_operations() -> None:
    """Demonstrate common user operations.

    Shows how to perform CRUD operations using UserRepository.
    """
    # Using the session context manager
    with get_session() as session:
        user_repo = UserRepository(session)

        # Create a new user
        new_user = User(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            permissions=UserPermission.STUDENT,
        )

        created_user = user_repo.create(new_user)
        print(f"Created user: {created_user.id} - {created_user.first_name} {created_user.last_name}")

        # Ensure we have a valid user ID for subsequent operations
        if created_user.id is None:
            print("Error: User ID is None after creation")
            return

        # Get user by ID
        fetched_user = user_repo.get_by_id(created_user.id)
        if fetched_user:
            print(f"Found user: {fetched_user.email}")

        # Get user by email
        user_by_email = user_repo.get_by_email("john.doe@example.com")
        if user_by_email:
            print(f"Found user by email: {user_by_email.first_name}")

        # List all students
        students = user_repo.list_users(permission=UserPermission.STUDENT)
        print(f"Found {len(students)} students")

        # Update user
        updated_user = user_repo.update(
            created_user.id, {"first_name": "Johnny", "permissions": UserPermission.INSTRUCTOR}
        )
        if updated_user:
            print(f"Updated user: {updated_user.first_name} is now an {updated_user.permissions.value}")

        # Search users by name
        john_users = user_repo.search_by_name("John")
        print(f"Found {len(john_users)} users with 'John' in their name")

        # Count instructors
        instructor_count = user_repo.count_by_permission(UserPermission.INSTRUCTOR)
        print(f"Total instructors: {instructor_count}")

        # Clean up - delete the user
        deleted = user_repo.delete(created_user.id)
        print(f"User deleted: {deleted}")


# FastAPI dependency example
def get_user_repository() -> UserRepository:
    """Provide dependency injection for FastAPI endpoints.

    Usage in FastAPI:
        @app.get("/users/{user_id}")
        def get_user(user_id: int, user_repo: UserRepository = Depends(get_user_repository)):
            return user_repo.get_by_id(user_id)
    """
    # Note: In a real FastAPI app, you'd want to use a dependency that manages
    # the session lifecycle properly. This is a simplified example.
    from src.core.database.session import create_session

    session = create_session()
    return UserRepository(session)


if __name__ == "__main__":
    # Run the example (only if database is available)
    try:
        example_user_operations()
    except Exception as e:
        print(f"Example failed (expected if database is not set up): {e}")
