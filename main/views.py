from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db import transaction, IntegrityError
from django.db.models import Q
from datetime import datetime, timedelta
from datetime import *
from django.http import Http404
# from .filters import CustomerFilter
# For displaying in template
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.template.loader import get_template
from .utils import render_to_pdf
# from dal import autocomplete
from django.http import JsonResponse,HttpResponse
from .forms import Signup, ReservationForm, CheckInRequestForm
from .models import Room, Reservation, Customer, Staff  # Import Models
import pytz


class GeneratePDF(generic.edit.View):
    def get(self,request, *args, **kwargs):
        # print(self.kwargs['id'])
        # return HttpResponse("HI")
        reservation = Reservation.objects.get(pk= self.kwargs['id'])
        print(reservation)
        template = get_template('invoice.html')
        context = {"reservation":reservation}
        html = template.render(context)
        pdf = render_to_pdf('invoice.html', context)
        return HttpResponse(pdf,content_type='application/pdf')

def index(request):
    """
    This is the view for homepage.
    This is a function based view.
    """
    page_title = _(
        "Hotel Management System")  # For page title as well as heading
    total_num_rooms = Room.objects.all().count()
    available_num_rooms = Room.objects.exclude(
        reservation__isnull=False).count()
    total_num_reservations = Reservation.objects.all().count()
    total_num_staffs = Staff.objects.all().count()
    total_num_customers = Customer.objects.all().count()
    if total_num_reservations == 0:
        last_reserved_by = Reservation.objects.none()
    else:
        last_reserved_by = Reservation.objects.get_queryset().latest('reservation_date_time')

    return render(
        request,
        'index1.html',
        # context is whatever sent to the template.
        # the index of the dictionary i.e. title in 'title': page_title
        # is used as variable in templates
        # where as the next one is the variable of this function
        {
            'title': page_title,
            'total_num_rooms': total_num_rooms,
            'available_num_rooms': available_num_rooms,
            'total_num_reservations': total_num_reservations,
            'total_num_staffs': total_num_staffs,
            'total_num_customers': total_num_customers,
            'last_reserved_by': last_reserved_by,
        }
    )


@transaction.atomic
def signup(request):
    title = "Signup"
    if request.user.is_authenticated:
        request.session.flush()
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    staffs_group = get_object_or_404(
                        Group, name__iexact="Staffs")
                    form.save()
                    staff_id = form.cleaned_data['staff_id']
                    username = form.cleaned_data['username']
                    s = get_object_or_404(Staff, staff_id__exact=staff_id)
                    s.user = get_object_or_404(User, username__iexact=username)
                    s.user.set_password(form.cleaned_data['password1'])
                    s.user.groups.add(staffs_group)
                    s.user.save()
                    s.user.save()
            except IntegrityError:
                raise Http404
            return redirect('index')
    else:
        form = Signup()

    return render(
        request,
        'signup.html', {
            'form': form, 'title': title},
    )


@permission_required('main.add_reservation', 'login', raise_exception=True)
@transaction.atomic
def reserve(request):
    title = "Add Reservation"
    reservation = Reservation.objects.none()
    if request.method == 'POST':
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            try:
                with transaction.atomic():
                    customer = Customer(
                        first_name=reservation_form.cleaned_data.get(
                            'first_name'),
                        middle_name=reservation_form.cleaned_data.get(
                            'middle_name'),
                        last_name=reservation_form.cleaned_data.get(
                            'last_name'),
                        email_address=reservation_form.cleaned_data.get(
                            'email'),
                        contact_no=reservation_form.cleaned_data.get(
                            'contact_no'),
                        address=reservation_form.cleaned_data.get('address'),
                    )
                    customer.save()
                    user = request.user
                    reservation = Reservation(
                        staff=get_object_or_404(Staff, user=user),
                        customer=customer,
                        no_of_children=reservation_form.cleaned_data.get(
                            'no_of_children'),
                        no_of_adults=reservation_form.cleaned_data.get(
                            'no_of_adults'),
                        expected_arrival_date_time=reservation_form.cleaned_data.get(
                            'expected_arrival_date_time'),
                        expected_departure_date_time=reservation_form.cleaned_data.get(
                            'expected_departure_date_time'),
                        reservation_date_time=timezone.now(),
                    )
                    reservation.save()
                    for room in reservation_form.cleaned_data.get('rooms'):
                        room.reservation = reservation
                        room.save()
            except IntegrityError:
                raise Http404
            return render(
                request,
                'reserve_success.html', {
                    'reservation': reservation,
                }
            )
    else:
        reservation_form = ReservationForm()

    return render(
        request,
        'reserve.html', {
            'title': title,
            'reservation_form': reservation_form,
        }
    )


def reserve_success(request):
    pass


# For generic ListView or DetailView, the default templates should be stored in templates/{{app_name}}/{{template_name}}
# By default template_name = modelName_list || modelName_detail.
# eg room_list, room_detail
# @permission_required('main.can_view_staff')
class RoomListView(PermissionRequiredMixin, generic.ListView):
    """
    View for list of rooms.
    Implements generic ListView.
    """
    model = Room  # Chooses the model for listing objects
    paginate_by = 10 # By how many objects this has to be paginated
    title = _("Room List")  # This is used for title and heading
    permission_required = 'main.can_view_room'

    # By default only objects of the model are sent as context
    # However extra context can be passed using field extra_context
    # Here title is passed.

    extra_context = {'title': title}

    # By default:
    # template_name = room_list
    # if you want to change it, use field template_name
    # here don't do this, since it is already done as default.
    # for own views, it can be done.

    def get_queryset(self):
        filter_value = self.request.GET.get('filter', 'all')
        if filter_value == 'all':
            filter_value = 0
        elif filter_value == 'avail':
            filter_value = 1
        try:
            new_context = Room.objects.filter(
                availability__in=[filter_value, 1])
        except ValidationError:
            raise Http404(_("Wrong filter argument given."))
        return new_context

    def get_context_data(self, **kwargs):
        context = super(RoomListView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', 'all')
        return context


class RoomDetailView(PermissionRequiredMixin, generic.DetailView):
    """
    View for detail of room
    Implements generic DetailView
    """
    # The remaining are same as previous.
    model = Room
    title = _("Room Information")
    permission_required = 'main.can_view_room'
    extra_context = {'title': title}


class ReservationListView(PermissionRequiredMixin, generic.ListView, generic.FormView):
    """
        View for list of reservations.
        Implements generic ListView.
        """
    model = Reservation
    # queryset field selects the objects to be displayed by the query.
    # Here, the objects are displayed by reservation date time in descending order
    queryset = Reservation.objects.all().order_by('-reservation_date_time')
    title = _("Reservation List")
    paginate_by = 10
    allow_empty = True
    form_class = CheckInRequestForm
    success_url = reverse_lazy('check_in-list')
    permission_required = 'main.can_view_reservation'
    extra_context = {'title': title}

   

    @transaction.atomic
    def form_valid(self, form):
        try:
            with transaction.atomic():
                checkin = form.save(commit=False)
                checkin.user = self.request.user
                checkin.save()
        except IntegrityError:
            raise Http404
        return super().form_valid(form)

    

class ReservationListView1(PermissionRequiredMixin, generic.ListView, generic.FormView):
    """
        View for list of reservations.
        Implements generic ListView.
        """
    model = Reservation


    # queryset field selects the objects to be displayed by the query.
    # Here, the objects are displayed by reservation date time in descending order
    # queryset = Reservation.objects.all().order_by('reservation_date_time')
    # week = datetime.today() + timedelta(days=7)
    # date = datetime.date.today()
    # startdate = date.today()
    enddate = date.today() + timedelta(days=6)

    queryset = Reservation.objects.filter(
        expected_arrival_date_time__range=[date.today(), enddate])
    # start_week = datetime.date.today() - datetime.timedelta(date.weekday())
    # end_week = start_week + datetime.timedelta(7)
    # queryset = Reservation.objects.filter(expected_arrival_date_time__range=[start_week, end_week])

    # import code
    # code.interact(local=dict(globals(), **locals()))
    # queryset = Reservation.objects.filter(
    #     expected_arrival_date_time__range=(t,week))
    # today = timezone.now()
    # current_week_num = today.isocalendar()[1]
    # queryset = Reservation.objects.filter(expected_arrival_date_time__gte=current_week_num).count()
    title = _("Reservation List")
    paginate_by = 10
    allow_empty = True
    form_class = CheckInRequestForm
    success_url = reverse_lazy('check_in-list')
    permission_required = 'main.can_view_reservation'
    extra_context = {'title': title}

    
    
    @transaction.atomic
    def form_valid(self, form):
        try:
            with transaction.atomic():
                checkin = form.save(commit=False)
                checkin.user = self.request.user
                checkin.save()
        except IntegrityError:
            raise Http404
        return super().form_valid(form)


class ReservationListView2(PermissionRequiredMixin, generic.ListView, generic.FormView):
    """
        View for list of reservations.
        Implements generic ListView.
        """
    model = Reservation
    # queryset field selects the objects to be displayed by the query.
    # Here, the objects are displayed by reservation date time in descending order
    # queryset = Reservation.objects.all().order_by('reservation_date_time')
    # month = datetime.today() + timedelta(days=30)
    # queryset = Reservation.objects.filter(expected_arrival_date_time__gte=month)
    queryset = Reservation.objects.filter(expected_arrival_date_time__gte=timezone.now().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0))

    title = _("Reservation List")
    paginate_by = 30
    allow_empty = True
    form_class = CheckInRequestForm
    success_url = reverse_lazy('check_in-list')
    permission_required = 'main.can_view_reservation'
    extra_context = {'title': title}

   

    @transaction.atomic
    def form_valid(self, form):
        try:
            with transaction.atomic():
                checkin = form.save(commit=False)
                checkin.user = self.request.user
                checkin.save()
        except IntegrityError:
            raise Http404
        return super().form_valid(form)

   
# def searchResults(request):
#     search=request.GET.get('searchinput')
#     print('search=',search)
#     quaryset = Reservation.objects.filter(customer__contains=search)
#     print(quaryset)
#     return render(request, 'search.html', {'quaryset': quaryset})

class ReservationListView3(PermissionRequiredMixin, generic.ListView, generic.FormView):
   
    model = Reservation

#     # queryset field selects the objects to be displayed by the query.
#     # Here, the objects are displayed by reservation date time in descending order
#     # queryset = Reservation.objects.all().order_by('reservation_date_time')
#     # month = datetime.today() + timedelta(days=30)
#     # queryset = Reservation.objects.filter(expected_arrival_date_time__gte=month)
    # queryset = Reservation.objects.filter(customer_first_name__icontains = 'anuj') 

    title = _("Reservation List")
    paginate_by = 30
    allow_empty = True
    form_class = CheckInRequestForm
    success_url = reverse_lazy('check_in-list')
    permission_required = 'main.can_view_reservation'
    extra_context = {'title': title}

    @transaction.atomic
    def form_valid(self, form):
        try:
            with transaction.atomic():
                checkin = form.save(commit=False)
                checkin.user = self.request.user
                checkin.save()
        except IntegrityError:
            raise Http404
        return super().form_valid(form)




class ReservationDetailView(PermissionRequiredMixin, generic.DetailView):
    """
    View for detail of reservation
    Implements generic DetailView
    """
    model = Reservation
    title = _("Reservation Information")
    permission_required = 'main.can_view_reservation'
    raise_exception = True
    extra_context = {'title': title}


class CustomerDetailView(PermissionRequiredMixin, generic.DetailView):
    """
    View for detail of customer
    Implements generic DetailView
    """
    model = Customer
    title = _("Customer Information")
    permission_required = 'main.can_view_customer'
    raise_exception = True
    extra_context = {'title': title}


class StaffDetailView(PermissionRequiredMixin, generic.DetailView):
    """
    View for detail of staff
    Implements generic DetailView
    """
    model = Staff
    title = _("Staff Information")
    permission_required = 'main.can_view_staff_detail'
    extra_context = {'title': title}


class ProfileView(generic.TemplateView):
    template_name = 'profile.html'
    title = "Profile"
    extra_context = {'title': title}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['information'] = get_object_or_404(
                Staff, user=self.request.user)
            context['user_information'] = self.request.user
        else:
            raise Http404("Your are not logged in.")
        return context


class GuestListView(PermissionRequiredMixin, generic.ListView):
    """
    View for list of guests present in hotel.
    """
    model = Customer
    paginate_by = 5
    allow_empty = True
    queryset = Customer.objects.all().filter(Q(reservation__checkin__isnull=False),
                                             Q(reservation__checkin__checkout__isnull=True))
    permission_required = 'main.can_view_customer'
    template_name = 'main/guest_list.html'
    title = 'Guest List View'
    context_object_name = 'guest_list'
    extra_context = {'title': title}



    
def contact(request):
    return render(request, 'main/contact.html')


def Gallery(request):
    return render(request, 'main/gallery.html')

# def autocompleteModel(request):
#     if request.is_ajax():
#         quaryset = Reservation.objects.filter(customer_first_name__startwith=request.REQUEST['search'])
#     results = []
#     for r in search_qs:
#         results.append(r.name)
#     resp = request.REQUEST['callback']+'('+ simpaljson.dumps(result)+ ');'
#     return HttpResponse(resp, content_type='application/json')


# def find_reservation_by_name(query_name):
#     qs = User.objects.all()
#     for term in query_name.split():
#         qs = qs.filter(Q(customer_first_name__icontains=term)
#                        | Q(customer_last_name__icontains=term))
#     return qs

# def search(request):
#     customer_list = Customer.objects.all()
#     quaryset = customer_list.objects.filter(customer_first_name = 'icontains')
