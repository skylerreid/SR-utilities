! program factorial_demo
!     implicit none
!     integer :: n, result

!     n = 5
!     result = factorial(n)

!     print *, "Factorial of", n, "is", result

! contains

!     function factorial(k) result(prod)
!         integer, intent(in) :: k
!         integer :: prod
!         integer :: i

!         prod = 1
!         do i = 1, k
!             prod = prod * i
!         end do
!     end function factorial

! end program factorial_demo

program factorial_demo
    implicit none
    integer:: n, result

    n = 5
    result = factorial(n)
    print *, "5 factorial is", result

    contains

    function factorial(k) result(prod)
        integer, intent(in) :: k
        integer :: prod
        integer :: i

        prod = 1
        do i = 1, k
            prod = prod*i
        end do
    end function factorial
end program factorial_demo