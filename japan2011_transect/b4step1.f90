subroutine b4step1(mbc,mx,meqn,q,xlower,dx,t,dt,maux,aux)

    ! Called before each call to step1.
    ! Use to set time-dependent aux arrays or perform other tasks.

    ! this version checks for negative depths 

    use geoclaw_module, only: dry_tolerance
    use setprob_module, only: hmax


    implicit none
    integer, intent(in) :: mbc,mx,meqn,maux
    real(kind=8), intent(in) :: xlower,dx,t,dt
    real(kind=8), intent(inout) :: q(meqn,1-mbc:mx+mbc)
    real(kind=8), intent(inout) :: aux(maux,1-mbc:mx+mbc)

    !local variables
    integer :: i,ig,j,m,mvars

      ! hmax:
      do i=1,mx
          hmax(i) = dmax1(hmax(i), q(1,i))
          enddo


      do i=1-mbc,mx+mbc
         if (q(1,i)<=dry_tolerance) then
            q(1,i) = max(q(1,i),0.0)
            do m=2,meqn
               q(m,i)=0.d0
            enddo
         endif
      enddo


end subroutine b4step1

