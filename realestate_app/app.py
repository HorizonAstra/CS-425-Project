from flask import Flask, render_template, redirect, url_for, flash, request
from flask_migrate import Migrate
from flask_login import (
    LoginManager, login_user, logout_user,
    current_user, login_required
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

from config import Config
from models import (
    db, User, Agent, Renter, Address, CreditCard,
    Property, House, Apartment, CommercialBuilding, Booking
)
from forms import (
    RegistrationForm, LoginForm, AddressForm,
    CreditCardForm, PropertyForm, SearchForm, BookingForm
)

from sqlalchemy import or_, and_

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(email):
    return User.query.get(email)


@app.route('/')
def index():
    return redirect(url_for('search'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.get(form.email.data):
            flash('Email already registered.', 'warning')
        else:
            u = User(
                email=form.email.data,
                full_name=form.full_name.data,
                user_type=form.user_type.data,
                password_hash=generate_password_hash(form.password.data)
            )
            db.session.add(u)
            if form.user_type.data == 'agent':
                db.session.add(Agent(email=u.email))
            else:
                db.session.add(Renter(email=u.email))
            db.session.commit()
            flash('Registered! Please log in.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.get(form.email.data)
        if u and check_password_hash(u.password_hash, form.password.data):
            login_user(u)
            return redirect(url_for('index'))
        flash('Invalid credentials.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


# ---- Profile: addresses & cards ----
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/address/add', methods=['GET', 'POST'])
@login_required
def add_address():
    form = AddressForm()
    if form.validate_on_submit():
        addr = Address(
            user_email=current_user.email,
            street=form.street.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data
        )
        db.session.add(addr)
        db.session.commit()
        flash('Address added.', 'success')
        return redirect(url_for('profile'))
    return render_template('address_form.html', form=form)


@app.route('/address/<int:aid>/edit', methods=['GET', 'POST'])
@login_required
def edit_address(aid):
    addr = Address.query.get_or_404(aid)
    if addr.user_email != current_user.email:
        flash('Not authorized.', 'danger')
        return redirect(url_for('profile'))
    form = AddressForm(obj=addr)
    if form.validate_on_submit():
        addr.street = form.street.data
        addr.city = form.city.data
        addr.state = form.state.data
        addr.zip_code = form.zip_code.data
        db.session.commit()
        flash('Address updated.', 'success')
        return redirect(url_for('profile'))
    return render_template('address_form.html', form=form)


@app.route('/address/<int:aid>/delete', methods=['POST'])
@login_required
def delete_address(aid):
    addr = Address.query.get_or_404(aid)
    if addr.user_email != current_user.email:
        flash('Not authorized.', 'danger')
    elif addr.cards:
        flash('Cannot delete address with linked credit cards.', 'warning')
    else:
        db.session.delete(addr)
        db.session.commit()
        flash('Address deleted.', 'info')
    return redirect(url_for('profile'))


@app.route('/card/add', methods=['GET', 'POST'])
@login_required
def add_card():
    if current_user.user_type != 'renter':
        flash('Only renters can add cards.', 'warning')
        return redirect(url_for('profile'))
    form = CreditCardForm()
    form.billing_address.choices = [
        (a.address_id, f"{a.street}, {a.city}") for a in current_user.addresses
    ]
    if form.validate_on_submit():
        card = CreditCard(
            card_number=form.card_number.data,
            renter_email=current_user.email,
            exp_date=form.exp_date.data,
            cvv=form.cvv.data,
            billing_address=form.billing_address.data
        )
        db.session.add(card)
        db.session.commit()
        flash('Card added.', 'success')
        return redirect(url_for('profile'))
    return render_template('cc_form.html', form=form)


@app.route('/card/<card_number>/edit', methods=['GET', 'POST'])
@login_required
def edit_card(card_number):
    card = CreditCard.query.get_or_404(card_number)
    if card.renter_email != current_user.email:
        flash('Not authorized.', 'danger')
        return redirect(url_for('profile'))
    form = CreditCardForm(obj=card)
    form.billing_address.choices = [
        (a.address_id, f"{a.street}, {a.city}") for a in current_user.addresses
    ]
    if form.validate_on_submit():
        card.exp_date = form.exp_date.data
        card.cvv = form.cvv.data
        card.billing_address = form.billing_address.data
        db.session.commit()
        flash('Card updated.', 'success')
        return redirect(url_for('profile'))
    return render_template('cc_form.html', form=form)


@app.route('/card/<card_number>/delete', methods=['POST'])
@login_required
def delete_card(card_number):
    card = CreditCard.query.get_or_404(card_number)
    if card.renter_email != current_user.email:
        flash('Not authorized.', 'danger')
    else:
        db.session.delete(card)
        db.session.commit()
        flash('Card deleted.', 'info')
    return redirect(url_for('profile'))


# ---- Agent: Property CRUD ----
@app.route('/property/add', methods=['GET', 'POST'])
@login_required
def add_property():
    if current_user.user_type != 'agent':
        flash('Only agents can add properties.', 'warning')
        return redirect(url_for('search'))
    form = PropertyForm()
    if form.validate_on_submit():
        p = Property(
            agent_email=current_user.email,
            property_type=form.property_type.data,
            street=form.street.data,
            city=form.city.data,
            state=form.state.data,
            price=form.price.data,
            available_from=form.available_from.data,
            available_to=form.available_to.data,
            sqr_footage=form.sqr_footage.data,
            description=form.description.data
        )
        db.session.add(p)
        db.session.flush()
        if p.property_type == 'house':
            db.session.add(House(
                property_id=p.property_id,
                num_rooms=form.num_rooms.data
            ))
        elif p.property_type == 'apartment':
            db.session.add(Apartment(
                property_id=p.property_id,
                num_rooms=form.num_rooms.data,
                building_type=form.building_type.data
            ))
        else:
            db.session.add(CommercialBuilding(
                property_id=p.property_id,
                business_type=form.business_type.data
            ))
        db.session.commit()
        flash('Property added.', 'success')
        return redirect(url_for('search'))
    return render_template('property_form.html', form=form)


@app.route('/property/<int:pid>/edit', methods=['GET', 'POST'])
@login_required
def edit_property(pid):
    p = Property.query.get_or_404(pid)
    if current_user.user_type != 'agent' or p.agent_email != current_user.email:
        flash('Not authorized.', 'danger')
        return redirect(url_for('search'))
    form = PropertyForm(obj=p)
    # populate subtype fields on GET
    if request.method == 'GET':
        form.property_type.data = p.property_type
        if p.house:
            form.num_rooms.data = p.house.num_rooms
        elif p.apartment:
            form.num_rooms.data = p.apartment.num_rooms
            form.building_type.data = p.apartment.building_type
        elif p.commercial:
            form.business_type.data = p.commercial.business_type
    if form.validate_on_submit():
        p.property_type = form.property_type.data
        p.street = form.street.data
        p.city = form.city.data
        p.state = form.state.data
        p.price = form.price.data
        p.available_from = form.available_from.data
        p.available_to = form.available_to.data
        p.sqr_footage = form.sqr_footage.data
        p.description = form.description.data

        # remove old subtype and add new
        if p.house:       db.session.delete(p.house)
        if p.apartment:   db.session.delete(p.apartment)
        if p.commercial:  db.session.delete(p.commercial)
        db.session.flush()

        if p.property_type == 'house':
            db.session.add(House(
                property_id=p.property_id,
                num_rooms=form.num_rooms.data
            ))
        elif p.property_type == 'apartment':
            db.session.add(Apartment(
                property_id=p.property_id,
                num_rooms=form.num_rooms.data,
                building_type=form.building_type.data
            ))
        else:
            db.session.add(CommercialBuilding(
                property_id=p.property_id,
                business_type=form.business_type.data
            ))

        db.session.commit()
        flash('Property updated.', 'success')
        return redirect(url_for('property_detail', pid=pid))
    return render_template('property_form.html', form=form)


@app.route('/property/<int:pid>/delete', methods=['POST'])
@login_required
def delete_property(pid):
    p = Property.query.get_or_404(pid)
    if current_user.user_type != 'agent' or p.agent_email != current_user.email:
        flash('Not authorized.', 'danger')
        return redirect(url_for('search'))
    else:
        db.session.delete(p)
        db.session.commit()
        flash('Property deleted.', 'info')
    return redirect(url_for('search'))


# ---- Search & Listing ----
@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    properties = []

    if form.validate_on_submit():
        loc          = form.location.data.strip()
        search_date  = form.date.data

        # --- base filters: location (street OR city OR state) + availability ---
        q = Property.query.filter(
            Property.available_from <= search_date,
            Property.available_to   >= search_date,
            or_(
                Property.city.ilike(f"%{loc}%"),
                Property.state.ilike(f"%{loc}%"),
                Property.street.ilike(f"%{loc}%")
            )
        )

        # --- exclude properties already booked for the requested date ---------
        q = q.filter(
            ~Property.bookings.any(
                and_(
                    Booking.start_date <= search_date,
                    Booking.end_date   >= search_date
                )
            )
        )

        # --- optional filters -------------------------------------------------
        if form.property_type.data:
            q = q.filter_by(property_type=form.property_type.data)

        if form.min_price.data is not None:
            q = q.filter(Property.price >= form.min_price.data)

        if form.max_price.data is not None:
            q = q.filter(Property.price <= form.max_price.data)

        # --- bedrooms filter (keep track if we already joined) ----------------
        joined_bed = False
        if form.min_bedrooms.data is not None:
            q = (q.outerjoin(House)
                   .outerjoin(Apartment)
                   .filter(
                       (House.num_rooms     >= form.min_bedrooms.data) |
                       (Apartment.num_rooms >= form.min_bedrooms.data)
                   ))
            joined_bed = True

        # --- ordering ---------------------------------------------------------
        if form.order_by.data == 'price':
            q = q.order_by(Property.price)
        else:  # bedrooms
            if not joined_bed:               # add the joins only once
                q = q.outerjoin(House).outerjoin(Apartment)
            q = q.order_by(
                House.num_rooms.nullslast(),
                Apartment.num_rooms.nullslast()
            )

        properties = q.all()

    return render_template('search.html', form=form, properties=properties)


@app.route('/property/<int:pid>')
@login_required
def property_detail(pid):
    p = Property.query.get_or_404(pid)
    return render_template('property_detail.html', p=p)


# ---- Booking ----
@app.route('/property/<int:pid>/book', methods=['GET', 'POST'])
@login_required
def book_property(pid):
    if current_user.user_type != 'renter':
        flash('Only renters can book.', 'warning')
        return redirect(url_for('property_detail', pid=pid))

    p = Property.query.get_or_404(pid)          # ← existing line
    form = BookingForm()
    form.card_number.choices = [(c.card_number, c.card_number)
                                for c in current_user.cards]

    if form.validate_on_submit():
        # ---- NEW AVAILABILITY CHECK ----------------------------------------
        if not (p.available_from <= form.start_date.data <= p.available_to and
                p.available_from <= form.end_date.data   <= p.available_to and
                form.start_date.data <= form.end_date.data):
            flash('Selected dates are outside this property’s availability window.',
                  'warning')
            return render_template('booking_form.html', form=form, p=p)
        # --------------------------------------------------------------------

        # monthly-rent total (inclusive months)
        months = ((form.end_date.data.year  - form.start_date.data.year) * 12 +
                  (form.end_date.data.month - form.start_date.data.month) + 1)
        total  = months * float(p.price)

        b = Booking(
            property_id=pid,
            renter_email=current_user.email,
            card_number=form.card_number.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            total_cost=total
        )
        db.session.add(b)
        db.session.commit()
        flash(f'Booked! Total cost: ${total:.2f}', 'success')
        return redirect(url_for('my_bookings'))

    return render_template('booking_form.html', form=form, p=p)


@app.route('/bookings')
@login_required
def my_bookings():
    if current_user.user_type == 'agent':
        return redirect(url_for('agent_bookings'))
    bs = Booking.query.filter_by(renter_email=current_user.email).all()
    return render_template('bookings.html', bookings=bs)


@app.route('/agent/bookings')
@login_required
def agent_bookings():
    if current_user.user_type != 'agent':
        return redirect(url_for('my_bookings'))
    bs = Booking.query.join(Property).filter(
        Property.agent_email == current_user.email
    ).all()
    return render_template('agent_bookings.html', bookings=bs)


@app.route('/booking/<int:bid>/cancel')
@login_required
def cancel_booking(bid):
    b = Booking.query.get_or_404(bid)
    if (current_user.user_type == 'renter' and b.renter_email != current_user.email) or \
       (current_user.user_type == 'agent' and b.property.agent_email != current_user.email):
        flash('Not authorized.', 'danger')
    else:
        db.session.delete(b)
        db.session.commit()
        flash('Booking canceled and refunded (simulated).', 'info')
    return redirect(
        url_for('my_bookings') if current_user.user_type == 'renter'
        else url_for('agent_bookings')
    )


if __name__ == '__main__':
    app.run(debug=True)
