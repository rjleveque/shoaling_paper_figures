subroutine qinit(meqn,mbc,mx,xlower,dx,q,maux,aux)

    ! Set initial conditions for the q array.
    ! This default version simply sets eta = max(h + b,0)

    ! For more specific initial conditions
    !  copy this to an application directory and
    !  loop over all grid cells to set values of q(1:meqn, 1:mx).

    use geoclaw_module, only: grav  !uncomment if needed
    use grid_module, only: xgrid,zgrid,mx_grid

    implicit none

    integer, intent(in) :: meqn,mbc,mx,maux
    real(kind=8), intent(in) :: xlower,dx
    real(kind=8), intent(in) :: aux(maux,1-mbc:mx+mbc)
    real(kind=8), intent(inout) :: q(meqn,1-mbc:mx+mbc)

    !locals
    integer :: i
    real(kind=8) :: xcell,x0,width,eta,xoff,x0sech2

    width = 80.e3
    x0sech2 = -200e3  ! initial center of sech2

    do i=1,mx
      xcell = 0.5*(xgrid(i) + xgrid(i+1))
      xoff = xcell-x0sech2
      if ((abs(xoff) < x0-width)) then 
          eta = 0.d0
        else
          eta = (2.d0 / (exp(3.d0*xoff/width) + exp(-3.d0*xoff/width)))**2
        endif
      q(1,i) = max(0.0, eta - aux(1,i))
      q(2,i) = eta*sqrt(grav*q(1,i))  ! right-going

   enddo


end subroutine qinit
