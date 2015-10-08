# init -1 python:
    # import types
    # from heapq import heappush, heappop
    # from itertools import count
    # from inspect import isgenerator
    # PY2 = True
    # if PY2:
        # import sys
    # Infinity = float('inf')  #: Convenience alias for infinity
    # PENDING = _object()
    # """Unique _object to identify pending values of events."""
    # URGENT = 0
    # """Priority of interrupts and process initialization events."""
    # NORMAL = 1
    # """Default priority used by events."""
# init python:
    # class BoundClass(_object):
        # """Allows classes to behave like methods.
#     
        # The ``__get__()`` descriptor is basically identical to
        # ``function.__get__()`` and binds the first argument of the ``cls`` to the
        # descriptor instance.
#     
        # """
        # def __init__(self, cls):
            # self.cls = cls
#     
        # def __get__(self, obj, type=None):
            # if obj is None:
                # return self.cls
            # return types.MethodType(self.cls, obj)
#     
        # @staticmethod
        # def bind_early(instance):
            # """Bind all :class:`BoundClass` attributes of the *instance's* class
            # to the instance itself to increase performance."""
            # cls = type(instance)
            # for name, obj in cls.__dict__.items():
                # if type(obj) is BoundClass:
                    # bound_class = getattr(instance, name)
                    # setattr(instance, name, bound_class)
#     
    # class _Event(_object):
        # """An event that may happen at some point in time.
#     
        # An event
#     
        # - may happen (:attr:`triggered` is ``False``),
        # - is going to happen (:attr:`triggered` is ``True``) or
        # - has happened (:attr:`processed` is ``True``).
#     
        # Every event is bound to an environment *env* and is initially not
        # triggered. _Events are scheduled for processing by the environment after
        # they are triggered by either :meth:`succeed`, :meth:`fail` or
        # :meth:`trigger`. These methods also set the *ok* flag and the *value* of
        # the event.
#     
        # An event has a list of :attr:`callbacks`. A callback can be any callable.
        # Once an event gets processed, all callbacks will be invoked with the event
        # as the single argument. Callbacks can check if the event was successful by
        # examining *ok* and do further processing with the *value* it has produced.
#     
        # Failed events are never silently ignored and will raise an exception upon
        # being processed. If a callback handles an exception, it must set *defused*
        # flag to ``True`` to prevent this.
#     
        # This class also implements ``__and__()`` (``&``) and ``__or__()`` (``|``).
        # If you concatenate two events using one of these operators,
        # a :class:`Condition` event is generated that lets you wait for both or one
        # of them.
#     
        # """
        # def __init__(self, env):
            # self.env = env
            # """The :class:`~simpy.core.Environment` the event lives in."""
            # self.callbacks = []
            # """List of functions that are called when the event is processed."""
            # self._value = PENDING
#     
        # def __repr__(self):
            # """Return the description of the event (see :meth:`_desc`) with the id
            # of the event."""
            # return '<%s _object at 0x%x>' % (self._desc(), id(self))
#     
        # def _desc(self):
            # """Return a string *_Event()*."""
            # return '%s()' % self.__class__.__name__
#     
        # @property
        # def triggered(self):
            # """Becomes ``True`` if the event has been triggered and its callbacks
            # are about to be invoked."""
            # return self._value is not PENDING
#     
        # @property
        # def processed(self):
            # """Becomes ``True`` if the event has been processed (e.g., its
            # callbacks have been invoked)."""
            # return self.callbacks is None
#     
        # @property
        # def value(self):
            # """The value of the event if it is available.
#     
            # The value is available when the event has been triggered.
#     
            # Raise a :exc:`AttributeError` if the value is not yet available.
#     
            # """
            # if self._value is PENDING:
                # raise AttributeError('Value of %s is not yet available' % self)
            # return self._value
#     
        # def trigger(self, event):
            # """Trigger the event with the state and value of the provided *event*.
            # Return *self* (this event instance).
#     
            # This method can be used directly as a callback function to trigger
            # chain reactions.
#     
            # """
            # self.ok = event.ok
            # self._value = event._value
            # self.env.schedule(self)
#     
        # def succeed(self, value=None):
            # """Set the event's value, mark it as successful and schedule it for
            # processing by the environment. Returns the event instance.
#     
            # Raise a :exc:`RuntimeError` if this event has already been triggerd.
#     
            # """
            # if self._value is not PENDING:
                # raise RuntimeError('%s has already been triggered' % self)
#     
            # self.ok = True
            # self._value = value
            # self.env.schedule(self)
            # return self
#     
        # def fail(self, exception):
            # """Set *exception* as the events value, mark it as failed and schedule
            # it for processing by the environment. Returns the event instance.
#     
            # Raise a :exc:`ValueError` if *exception* is not an :exc:`Exception`.
#     
            # Raise a :exc:`RuntimeError` if this event has already been triggered.
#     
            # """
            # if self._value is not PENDING:
                # raise RuntimeError('%s has already been triggered' % self)
            # if not isinstance(exception, BaseException):
                # raise ValueError('%s is not an exception.' % exception)
            # self.ok = False
            # self._value = exception
            # self.env.schedule(self)
            # return self
#     
        # def __and__(self, other):
            # """Return a :class:`~simpy.events.Condition` that will be triggered if
            # both, this event and *other*, have been processed."""
            # return Condition(self.env, Condition.all_events, [self, other])
#     
        # def __or__(self, other):
            # """Return a :class:`~simpy.events.Condition` that will be triggered if
            # either this event or *other* have been processed (or even both, if they
            # happened concurrently)."""
            # return Condition(self.env, Condition.any_events, [self, other])
#     
#     
    # class Timeout(_Event):
        # """A :class:`~simpy.events._Event` that gets triggered after a *delay* has
        # passed.
#     
        # This event is automatically triggered when it is created.
#     
        # """
        # def __init__(self, env, delay, value=None):
            # if delay < 0:
                # raise ValueError('Negative delay %s' % delay)
            # # NOTE: The following initialization code is inlined from
            # # _Event.__init__() for performance reasons.
            # self.env = env
            # self.callbacks = []
            # self._value = value
            # self._delay = delay
            # self.ok = True
            # env.schedule(self, NORMAL, delay)
#     
        # def _desc(self):
            # """Return a string *Timeout(delay[, value=value])*."""
            # return '%s(%s%s)' % (self.__class__.__name__, self._delay,
                                 # '' if self._value is None else
                                 # (', value=%s' % self._value))
#     
#     
    # class Initialize(_Event):
        # """Initializes a process. Only used internally by :class:`Process`.
#     
        # This event is automatically triggered when it is created.
#     
        # """
        # def __init__(self, env, process):
            # # NOTE: The following initialization code is inlined from
            # # _Event.__init__() for performance reasons.
            # self.env = env
            # self.callbacks = [process._resume]
            # self._value = None
#     
            # # The initialization events needs to be scheduled as urgent so that it
            # # will be handled before interrupts. Otherwise a process whose
            # # generator has not yet been started could be interrupted.
            # self.ok = True
            # env.schedule(self, URGENT)
#     
#     
    # class Interruption(_Event):
        # """Immediately schedules an :class:`Interrupt` exception with the given
        # *cause* to be thrown into *process*.
#     
        # This event is automatically triggered when it is created.
#     
        # """
        # def __init__(self, process, cause):
            # # NOTE: The following initialization code is inlined from
            # # _Event.__init__() for performance reasons.
            # self.env = process.env
            # self.callbacks = [self._interrupt]
            # self._value = Interrupt(cause)
            # self.ok = False
            # self.defused = True
#     
            # if process._value is not PENDING:
                # raise RuntimeError('%s has terminated and cannot be interrupted.' %
                                   # process)
#     
            # if process is self.env.active_process:
                # raise RuntimeError('A process is not allowed to interrupt itself.')
#     
            # self.process = process
            # self.env.schedule(self, URGENT)
#     
        # def _interrupt(self, event):
            # # Ignore dead processes. Multiple concurrently scheduled interrupts
            # # cause this situation. If the process dies while handling the first
            # # one, the remaining interrupts must be ignored.
            # if self.process._value is not PENDING:
                # return
#     
            # # A process never expects an interrupt and is always waiting for a
            # # target event. Remove the process from the callbacks of the target.
            # self.process._target.callbacks.remove(self.process._resume)
#     
            # self.process._resume(self)
#     
#     
    # class Process(_Event):
        # """Process an event yielding generator.
#     
        # A generator (also known as a coroutine) can suspend its execution by
        # yielding an event. ``Process`` will take care of resuming the generator
        # with the value of that event once it has happened. The exception of failed
        # events is thrown into the generator.
#     
        # ``Process`` itself is an event, too. It is triggered, once the generator
        # returns or raises an exception. The value of the process is the return
        # value of the generator or the exception, respectively.
#     
        # .. note::
#     
           # Python version prior to 3.3 do not support return statements in
           # generators. You can use :meth:~simpy.core.Environment.exit() as
           # a workaround.
#     
        # Processes can be interrupted during their execution by :meth:`interrupt`.
#     
        # """
        # def __init__(self, env, generator):
            # if not isgenerator(generator):
                # raise ValueError('%s is not a generator.' % generator)
#     
            # # NOTE: The following initialization code is inlined from
            # # _Event.__init__() for performance reasons.
            # self.env = env
            # self.callbacks = []
            # self._value = PENDING
#     
            # self._generator = generator
#     
            # # Schedule the start of the execution of the process.
            # self._target = Initialize(env, self)
#     
        # def _desc(self):
            # """Return a string *Process(process_func_name)*."""
            # return '%s(%s)' % (self.__class__.__name__, self._generator.__name__)
#     
        # @property
        # def target(self):
            # """The event that the process is currently waiting for.
#     
            # Returns ``None`` if the process is dead or it is currently being
            # interrupted.
#     
            # """
            # return self._target
#     
        # @property
        # def is_alive(self):
            # """``True`` until the process generator exits."""
            # return self._value is PENDING
#     
        # def interrupt(self, cause=None):
            # """Interupt this process optionally providing a *cause*.
#     
            # A process cannot be interrupted if it already terminated. A process can
            # also not interrupt itself. Raise a :exc:`RuntimeError` in these
            # cases.
#     
            # """
            # Interruption(self, cause)
#     
        # def _resume(self, event):
            # """Resumes the execution of the process with the value of *event*. If
            # the process generator exits, the process itself will get triggered with
            # the return value or the exception of the generator."""
            # # Mark the current process as active.
            # self.env._active_proc = self
#     
            # while True:
                # # Get next event from process
                # try:
                    # if event.ok:
                        # event = self._generator.send(event._value)
                    # else:
                        # # The process has no choice but to handle the failed event
                        # # (or fail itself).
                        # event.defused = True
#     
                        # # Create an exclusive copy of the exception for this
                        # # process to prevent traceback modifications by other
                        # # processes.
                        # exc = type(event._value)(*event._value.args)
                        # exc.__cause__ = event._value
                        # if PY2:
                            # if hasattr(event._value, '__traceback__'):
                                # exc.__traceback__ = event._value.__traceback__
                        # event = self._generator.throw(exc)
                # except StopIteration as e:
                    # # Process has terminated.
                    # event = None
                    # self.ok = True
                    # self._value = e.args[0] if len(e.args) else None
                    # self.env.schedule(self)
                    # break
                # except BaseException as e:
                    # # Process has failed.
                    # event = None
                    # self.ok = False
                    # tb = e.__traceback__ if not PY2 else sys.exc_info()[2]
                    # # Strip the frame of this function from the traceback as it
                    # # does not add any useful information.
                    # e.__traceback__ = tb.tb_next
                    # self._value = e
                    # self.env.schedule(self)
                    # break
#     
                # # Process returned another event to wait upon.
                # try:
                    # # Be optimistic and blindly access the callbacks attribute.
                    # if event.callbacks is not None:
                        # # The event has not yet been triggered. Register callback
                        # # to resume the process if that happens.
                        # event.callbacks.append(self._resume)
                        # break
                # except AttributeError:
                    # # Our optimism didn't work out, figure out what went wrong and
                    # # inform the user.
                    # if not hasattr(event, 'callbacks'):
                        # msg = 'Invalid yield value "%s"' % event
#     
                    # descr = _describe_frame(self._generator.gi_frame)
                    # error = RuntimeError('\n%s%s' % (descr, msg))
                    # # Drop the AttributeError as the cause for this exception.
                    # error.__cause__ = None
                    # raise error
#     
            # self._target = event
            # self.env._active_proc = None
#     
#     
    # class ConditionValue(_object):
        # """Result of a :class:`~simpy.events.Condition`. It supports convenient
        # dict-like access to the triggered events and their values. The events are
        # ordered by their occurences in the condition."""
#     
        # def __init__(self):
            # self.events = []
#     
        # def __getitem__(self, key):
            # if key not in self.events:
                # raise KeyError(str(key))
#     
            # return key._value
#     
        # def __contains__(self, key):
            # return key in self.events
#     
        # def __eq__(self, other):
            # if type(other) is ConditionValue:
                # return self.events == other.events
#     
            # return self.todict() == other
#     
        # def __repr__(self):
            # return '<ConditionValue %s>' % self.todict()
#     
        # def __iter__(self):
            # return self.keys()
#     
        # def keys(self):
            # return (event for event in self.events)
#     
        # def values(self):
            # return (event._value for event in self.events)
#     
        # def items(self):
            # return ((event, event._value) for event in self.events)
#     
        # def todict(self):
            # return dict((event, event._value) for event in self.events)
#     
#     
    # class Condition(_Event):
        # """An event that gets triggered once the condition function *evaluate*
        # returns ``True`` on the given list of *events*.
#     
        # The value of the condition event is an instance of :class:`ConditionValue`
        # which allows convenient access to the input events and their values. The
        # :class:`ConditionValue` will only contain entries for those events that
        # occurred before the condition is processed.
#     
        # If one of the events fails, the condition also fails and forwards the
        # exception of the failing event.
#     
        # The *evaluate* function receives the list of target events and the number
        # of processed events in this list: ``evaluate(events, processed_count)``. If
        # it returns ``True``, the condition is triggered. The
        # :func:`Condition.all_events()` and :func:`Condition.any_events()` functions
        # are used to implement *and* (``&``) and *or* (``|``) for events.
#     
        # Condition events can be nested.
#     
        # """
        # def __init__(self, env, evaluate, events):
            # super(Condition, self).__init__(env)
            # self._evaluate = evaluate
            # self._events = events if type(events) is tuple else tuple(events)
            # self._count = 0
#     
            # if not self._events:
                # # Immediately succeed if no events are provided.
                # self.succeed(ConditionValue())
                # return
#     
            # # Check if events belong to the same environment.
            # for event in self._events:
                # if self.env != event.env:
                    # raise ValueError('It is not allowed to mix events from '
                                     # 'different environments')
#     
            # # Check if the condition is met for each processed event. Attach
            # # _check() as a callback otherwise.
            # for event in self._events:
                # if event.callbacks is None:
                    # self._check(event)
                # else:
                    # event.callbacks.append(self._check)
#     
            # # Register a callback which will build the value of this condition
            # # after it has been triggered.
            # self.callbacks.append(self._build_value)
#     
        # def _desc(self):
            # """Return a string *Condition(evaluate, [events])*."""
            # return '%s(%s, %s)' % (self.__class__.__name__,
                                   # self._evaluate.__name__, self._events)
#     
        # def _populate_value(self, value):
            # """Populate the *value* by recursively visiting all nested
            # conditions."""
#     
            # for event in self._events:
                # if isinstance(event, Condition):
                    # event._populate_value(value)
                # elif event.callbacks is None:
                    # value.events.append(event)
#     
        # def _build_value(self, event):
            # """Build the value of this condition."""
            # if event.ok:
                # self._value = ConditionValue()
                # self._populate_value(self._value)
#     
        # def _check(self, event):
            # """Check if the condition was already met and schedule the *event* if
            # so."""
            # if self._value is not PENDING:
                # return
#     
            # self._count += 1
#     
            # if not event.ok:
                # # Abort if the event has failed.
                # event.defused = True
                # self.fail(event._value)
            # elif self._evaluate(self._events, self._count):
                # # The condition has been met. The _collect_values callback will
                # # populate set the value once this condition gets processed.
                # self.succeed()
#     
        # @staticmethod
        # def all_events(events, count):
            # """An evaluation function that returns ``True`` if all *events* have
            # been triggered."""
            # return len(events) == count
#     
        # @staticmethod
        # def any_events(events, count):
            # """An evaluation function that returns ``True`` if at least one of
            # *events* has been triggered."""
            # return count > 0 or len(events) == 0
#     
#     
#     
# 
#     
    # class AllOf(Condition):
        # """A :class:`~simpy.events.Condition` event that is triggered if all of
        # a list of *events* have been successfully triggered. Fails immediately if
        # any of *events* failed.
#     
        # """
        # def __init__(self, env, events):
            # super(AllOf, self).__init__(env, Condition.all_events, events)
#     
#     
    # class AnyOf(Condition):
        # """A :class:`~simpy.events.Condition` event that is triggered if any of
        # a list of *events* has been successfully triggered. Fails immediately if
        # any of *events* failed.
#     
        # """
        # def __init__(self, env, events):
            # super(AnyOf, self).__init__(env, Condition.any_events, events)
#     
#     
    # class Interrupt(Exception):
        # """Exception thrown into a process if it is interrupted (see
        # :func:`~simpy.events.Process.interrupt()`).
#     
        # :attr:`cause` provides the reason for the interrupt, if any.
#     
        # If a process is interrupted concurrently, all interrupts will be thrown
        # into the process in the same order as they occurred.
#     
#     
        # """
        # def __str__(self):
            # return '%s(%r)' % (self.__class__.__name__, self.cause)
#     
        # @property
        # def cause(self):
            # """The cause of the interrupt or ``None`` if no cause was provided."""
            # return self.args[0]
#     
#     
    # def _describe_frame(frame):
        # """Print filename, line number and function name of a stack frame."""
        # filename, name = frame.f_code.co_filename, frame.f_code.co_name
        # lineno = frame.f_lineno
#     
        # with open(filename) as f:
            # for no, line in enumerate(f):
                # if no + 1 == lineno:
                    # break
#     
        # return '  File "%s", line %d, in %s\n    %s\n' % (filename, lineno, name,
                                                          # line.strip())
#         
# 
    # class Put(_Event):
        # """Generic event for requesting to put something into the *resource*.
#     
        # This event (and all of its subclasses) can act as context manager and can
        # be used with the :keyword:`with` statement to automatically cancel the
        # request if an exception (like an :class:`simpy.events.Interrupt` for
        # example) occurs:
#     
        # .. code-block:: python
#     
            # with res.put(item) as request:
                # yield request
#     
        # """
        # def __init__(self, resource):
            # super(Put, self).__init__(resource._env)
            # self.resource = resource
            # self.proc = self.env.active_process
#     
            # resource.put_queue.append(self)
            # self.callbacks.append(resource._trigger_get)
            # resource._trigger_put(None)
#     
        # def __enter__(self):
            # return self
#     
        # def __exit__(self, exc_type, exc_value, traceback):
            # self.cancel()
#     
        # def cancel(self):
            # """Cancel this put request.
#     
            # This method has to be called if the put request must be aborted, for
            # example if a process needs to handle an exception like an
            # :class:`~simpy.events.Interrupt`.
#     
            # If the put request was created in a :keyword:`with` statement, this
            # method is called automatically.
#     
            # """
            # if not self.triggered:
                # self.resource.put_queue.remove(self)
#     
#     
    # class Get(_Event):
        # """Generic event for requesting to get something from the *resource*.
#     
        # This event (and all of its subclasses) can act as context manager and can
        # be used with the :keyword:`with` statement to automatically cancel the
        # request if an exception (like an :class:`simpy.events.Interrupt` for
        # example) occurs:
#     
        # .. code-block:: python
#     
            # with res.put(item) as request:
                # yield request
#     
        # """
        # def __init__(self, resource):
            # super(Get, self).__init__(resource._env)
            # self.resource = resource
            # self.proc = self.env.active_process
#     
            # resource.get_queue.append(self)
            # self.callbacks.append(resource._trigger_put)
            # resource._trigger_get(None)
#     
        # def __enter__(self):
            # return self
#     
        # def __exit__(self, exc_type, exc_value, traceback):
            # self.cancel()
#     
        # def cancel(self):
            # """Cancel this get request.
#     
            # This method has to be called if the get request must be aborted, for
            # example if a process needs to handle an exception like an
            # :class:`~simpy.events.Interrupt`.
#     
            # If the get request was created in a :keyword:`with` statement, this
            # method is called automatically.
#     
            # """
            # if not self.triggered:
                # self.resource.get_queue.remove(self)
#     
#     
    # class BaseResource(_object):
        # """Abstract base class for a shared resource.
#     
        # You can :meth:`put()` something into the resources or :meth:`get()`
        # something out of it. Both methods return an event that is triggered once
        # the operation is completed. If a :meth:`put()` request cannot complete
        # immediately (for example if the resource has reached a capacity limit) it
        # is enqueued in the :attr:`put_queue` for later processing. Likewise for
        # :meth:`get()` requests.
#     
        # Subclasses can customize the resource by:
#     
        # - providing custom :attr:`PutQueue` and :attr:`GetQueue` types,
        # - providing custom :class:`Put` respectively :class:`Get` events,
        # - and implementing the request processing behaviour through the methods
          # ``_do_get()`` and ``_do_put()``.
#     
        # """
        # PutQueue = list
        # """The type to be used for the :attr:`put_queue`. It is a plain
        # :class:`list` by default. The type must support index access (e.g.
        # ``__getitem__()`` and ``__len__()``) as well as provide ``append()`` and
        # ``pop()`` operations."""
#     
        # GetQueue = list
        # """The type to be used for the :attr:`get_queue`. It is a plain
        # :class:`list` by default. The type must support index access (e.g.
        # ``__getitem__()`` and ``__len__()``) as well as provide ``append()`` and
        # ``pop()`` operations."""
#     
        # def __init__(self, env, capacity):
            # self._env = env
            # self._capacity = capacity
            # self.put_queue = self.PutQueue()
            # """Queue of pending *put* requests."""
            # self.get_queue = self.GetQueue()
            # """Queue of pending *get* requests."""
#     
            # # Bind event constructors as methods
            # BoundClass.bind_early(self)
#     
        # @property
        # def capacity(self):
            # """Maximum capacity of the resource."""
            # return self._capacity
#     
        # put = BoundClass(Put)
        # """Request to put something into the resource and return a :class:`Put`
        # event, which gets triggered once the request succeeds."""
#     
        # get = BoundClass(Get)
        # """Request to get something from the resource and return a :class:`Get`
        # event, which gets triggered once the request succeeds."""
#     
        # def _do_put(self, event):
            # """Perform the *put* operation.
#     
            # This method needs to be implemented by subclasses. If the conditions
            # for the put *event* are met, the method must trigger the event (e.g.
            # call :meth:`_Event.succeed()` with an apropriate value).
#     
            # This method is called by :meth:`_trigger_put` for every event in the
            # :attr:`put_queue`, as long as the return value does not evaluate
            # ``False``.
            # """
            # raise NotImplementedError(self)
#     
        # def _trigger_put(self, get_event):
            # """This method is called once a new put event has been created or a get
            # event has been processed.
#     
            # The method iterates over all put events in the :attr:`put_queue` and
            # calls :meth:`_do_put` to check if the conditions for the event are met.
            # If :meth:`_do_put` returns ``False``, the iteration is stopped early.
            # """
#     
            # # Maintain queue invariant: All put requests must be untriggered.
            # # This code is not very pythonic because the queue interface should be
            # # simple (only append(), pop(), __getitem__() and __len__() are
            # # required).
            # idx = 0
            # while idx < len(self.put_queue):
                # put_event = self.put_queue[idx]
                # proceed = self._do_put(put_event)
                # if put_event.triggered:
                    # # @ FIXED ASSERTION ERROR
                    # try:
                        # self.put_queue.pop(idx) == put_event
                    # except:
                        # pass
                # else:
                    # idx += 1
#     
                # if not proceed:
                    # break
#     
        # def _do_get(self, event):
            # """Perform the *get* operation.
#     
            # This method needs to be implemented by subclasses. If the conditions
            # for the get *event* are met, the method must trigger the event (e.g.
            # call :meth:`_Event.succeed()` with an apropriate value).
#     
            # This method is called by :meth:`_trigger_get` for every event in the
            # :attr:`get_queue`, as long as the return value does not evaluate
            # ``False``.
            # """
            # raise NotImplementedError(self)
#     
        # def _trigger_get(self, put_event):
            # """Trigger get events.
#     
            # This method is called once a new get event has been created or a put
            # event has been processed.
#     
            # The method iterates over all get events in the :attr:`get_queue` and
            # calls :meth:`_do_get` to check if the conditions for the event are met.
            # If :meth:`_do_get` returns ``False``, the iteration is stopped early.
            # """
#     
            # # Maintain queue invariant: All get requests must be untriggered.
            # # This code is not very pythonic because the queue interface should be
            # # simple (only append(), pop(), __getitem__() and __len__() are
            # # required).
            # idx = 0
            # while idx < len(self.get_queue):
                # get_event = self.get_queue[idx]
                # proceed = self._do_get(get_event)
                # if get_event.triggered:
                    # # @ FIXED ASSERTION ERROR
                    # try:
                        # self.get_queue.pop(idx) == get_event
                    # except:
                        # pass
                # else:
                    # idx += 1
#     
                # if not proceed:
                    # break
#                     
    # class ContainerPut(Put):
        # """Request to put *amount* of matter into the *container*. The request will
        # be triggered once there is enough space in the *container* available.
#     
        # Raise a :exc:`ValueError` if ``amount <= 0``.
#     
        # """
        # def __init__(self, container, amount):
            # if amount <= 0:
                # raise ValueError('amount(=%s) must be > 0.' % amount)
            # self.amount = amount
            # """The amount of matter to be put into the container."""
#     
            # super(ContainerPut, self).__init__(container)
#     
#     
    # class ContainerGet(Get):
        # """Request to get *amount* of matter from the *container*. The request will
        # be triggered once there is enough matter available in the *container*.
#     
        # Raise a :exc:`ValueError` if ``amount <= 0``.
#     
        # """
        # def __init__(self, container, amount):
            # if amount <= 0:
                # raise ValueError('amount(=%s) must be > 0.' % amount)
            # self.amount = amount
            # """The amount of matter to be taken out of the container."""
#     
            # super(ContainerGet, self).__init__(container)
#     
#     
    # class Container(BaseResource):
        # """Resource containing up to *capacity* of matter which may either be
        # continuous (like water) or discrete (like apples). It supports requests to
        # put or get matter into/from the container.
#     
        # The *env* parameter is the :class:`~simpy.core.Environment` instance the
        # container is bound to.
#     
        # The *capacity* defines the size of the container. By default, a container
        # is of unlimited size. The initial amount of matter is specified by *init*
        # and defaults to ``0``.
#     
        # Raise a :exc:`ValueError` if ``capacity <= 0``, ``init < 0`` or
        # ``init > capacity``.
#     
        # """
        # def __init__(self, env, capacity=float('inf'), init=0):
            # if capacity <= 0:
                # raise ValueError('"capacity" must be > 0.')
            # if init < 0:
                # raise ValueError('"init" must be >= 0.')
            # if init > capacity:
                # raise ValueError('"init" must be <= "capacity".')
#     
            # super(Container, self).__init__(env, capacity)
#     
            # self._level = init
#     
        # @property
        # def level(self):
            # """The current amount of the matter in the container."""
            # return self._level
#     
        # put = BoundClass(ContainerPut)
        # """Request to put *amount* of matter into the container."""
#     
        # get = BoundClass(ContainerGet)
        # """Request to get *amount* of matter out of the container."""
#     
        # def _do_put(self, event):
            # if self._capacity - self._level >= event.amount:
                # self._level += event.amount
                # event.succeed()
                # return True
#     
        # def _do_get(self, event):
            # if self._level >= event.amount:
                # self._level -= event.amount
                # event.succeed()
                # return True
#                 
# 
    # class Preempted(_object):
        # """Cause of an preemption :class:`~simpy.events.Interrupt` containing
        # information about the preemption.
#     
        # """
        # def __init__(self, by, usage_since):
            # self.by = by
            # """The preempting :class:`simpy.events.Process`."""
            # self.usage_since = usage_since
            # """The simulation time at which the preempted process started to use
            # the resource."""
#     
#     
    # class Request(Put):
        # """Request usage of the *resource*. The event is triggered once access is
        # granted. Subclass of :class:`simpy.resources.Put`.
#     
        # If the maximum capacity of users has not yet been reached, the request is
        # triggered immediately. If the maximum capacity has been
        # reached, the request is triggered once an earlier usage request on the
        # resource is released.
#     
        # The request is automatically released when the request was created within
        # a :keyword:`with` statement.
#     
        # """
        # def __exit__(self, exc_type, value, traceback):
            # super(Request, self).__exit__(exc_type, value, traceback)
            # self.resource.release(self)
#     
#     
    # class Release(Get):
        # """Releases the usage of *resource* granted by *request*. This event is
        # triggered immediately. Subclass of :class:`simpy.resources.Get`.
#     
        # """
        # def __init__(self, resource, request):
            # self.request = request
            # """The request (:class:`Request`) that is to be released."""
            # super(Release, self).__init__(resource)
#     
#     
    # class PriorityRequest(Request):
        # """Request the usage of *resource* with a given *priority*. If the
        # *resource* supports preemption and *preempt* is ``True`` other usage
        # requests of the *resource* may be preempted (see
        # :class:`PreemptiveResource` for details).
#     
        # This event type inherits :class:`Request` and adds some additional
        # attributes needed by :class:`PriorityResource` and
        # :class:`PreemptiveResource`
#     
        # """
        # def __init__(self, resource, priority=0, preempt=True):
            # self.priority = priority
            # """The priority of this request. A smaller number means higher
            # priority."""
#     
            # self.preempt = preempt
            # """Indicates whether the request should preempt a resource user or not
            # (:class:`PriorityResource` ignores this flag)."""
#     
            # self.time = resource._env.now
            # """The time at which the request was made."""
#     
            # self.key = (self.priority, self.time, not self.preempt)
            # """Key for sorting events. Consists of the priority (lower value is
            # more important), the time at which the request was made (earlier
            # requests are more important) and finally the preemption flag (preempt
            # requests are more important)."""
#     
            # super(PriorityRequest, self).__init__(resource)
#     
#     
    # class SortedQueue(list):
        # """Queue for sorting events by their :attr:`~PriorityRequest.key`
        # attribute.
#     
        # """
        # def __init__(self, maxlen=None):
            # super(SortedQueue, self).__init__()
            # self.maxlen = maxlen
            # """Maximum length of the queue."""
#     
        # def append(self, item):
            # """Sort *item* into the queue.
#     
            # Raise a :exc:`RuntimeError` if the queue is full.
#     
            # """
            # if self.maxlen is not None and len(self) >= self.maxlen:
                # raise RuntimeError('Cannot append event. Queue is full.')
#     
            # super(SortedQueue, self).append(item)
            # super(SortedQueue, self).sort(key=lambda e: e.key)
#     
#     
    # class Resource(BaseResource):
        # """Resource with *capacity* of usage slots that can be requested by
        # processes.
#     
        # If all slots are taken, requests are enqueued. Once a usage request is
        # released, a pending request will be triggered.
#     
        # The *env* parameter is the :class:`~simpy.core.Environment` instance the
        # resource is bound to.
#     
        # """
        # def __init__(self, env, capacity=1):
            # if capacity <= 0:
                # raise ValueError('"capacity" must be > 0.')
#     
            # super(Resource, self).__init__(env, capacity)
#     
            # self.users = []
            # """List of :class:`Request` events for the processes that are currently
            # using the resource."""
            # self.queue = self.put_queue
            # """Queue of pending :class:`Request` events. Alias of
            # :attr:`~simpy.resources.BaseResource.put_queue`.
            # """
#     
        # @property
        # def count(self):
            # """Number of users currently using the resource."""
            # return len(self.users)
#     
        # request = BoundClass(Request)
        # """Request a usage slot."""
#     
        # release = BoundClass(Release)
        # """Release a usage slot."""
#     
        # def _do_put(self, event):
            # if len(self.users) < self.capacity:
                # self.users.append(event)
                # event.succeed()
#     
        # def _do_get(self, event):
            # try:
                # self.users.remove(event.request)
            # except ValueError:
                # pass
            # event.succeed()
#     
#     
    # class PriorityResource(Resource):
        # """A :class:`~simpy.resources.resource.Resource` supporting prioritized
        # requests.
#     
        # Pending requests in the :attr:`~Resource.queue` are sorted in ascending
        # order by their *priority* (that means lower values are more important).
#     
        # """
        # PutQueue = SortedQueue
        # """Type of the put queue. See
        # :attr:`~simpy.resources.BaseResource.put_queue` for details."""
        # GetQueue = list
        # """Type of the get queue. See
        # :attr:`~simpy.resources.BaseResource.get_queue` for details."""
#     
        # def __init__(self, env, capacity=1):
            # super(PriorityResource, self).__init__(env, capacity)
#     
        # request = BoundClass(PriorityRequest)
        # """Request a usage slot with the given *priority*."""
#     
        # release = BoundClass(Release)
        # """Release a usage slot."""
#     
#     
    # class PreemptiveResource(PriorityResource):
        # """A :class:`~simpy.resources.resource.PriorityResource` with preemption.
#     
        # If a request is preempted, the process of that request will receive an
        # :class:`~simpy.events.Interrupt` with a :class:`Preempted` instance as
        # cause.
#     
        # """
        # def _do_put(self, event):
            # if len(self.users) >= self.capacity and event.preempt:
                # # Check if we can preempt another process
                # preempt = sorted(self.users, key=lambda e: e.key)[-1]
                # if preempt.key > event.key:
                    # self.users.remove(preempt)
                    # preempt.proc.interrupt(Preempted(by=event.proc,
                                                     # usage_since=preempt.time))
#     
            # return super(PreemptiveResource, self)._do_put(event)
#             
#     
    # class StorePut(Put):
        # """Request to put *item* into the *store*. The request is triggered once
        # there is space for the item in the store.
#     
        # """
        # def __init__(self, store, item):
            # self.item = item
            # """The item to put into the store."""
            # super(StorePut, self).__init__(store)
#     
#     
    # class StoreGet(Get):
        # """Request to get an *item* from the *store*. The request is triggered
        # once there is an item available in the store.
#     
        # """
        # pass
#     
#     
    # class FilterStoreGet(StoreGet):
        # """Request to get an *item* from the *store* matching the *filter*. The
        # request is triggered once there is such an item available in the store.
#     
        # *filter* is a function receiving one item. It should return ``True`` for
        # items matching the filter criterion. The default function returns ``True``
        # for all items, which makes the request to behave exactly like
        # :class:`StoreGet`.
#     
        # """
        # def __init__(self, resource, filter=lambda item: True):
            # self.filter = filter
            # """The filter function to filter items in the store."""
            # super(FilterStoreGet, self).__init__(resource)
#     
#     
    # class Store(BaseResource):
        # """Resource with *capacity* slots for storing arbitrary _objects. By
        # default, the *capacity* is unlimited and _objects are put and retrieved from
        # the store in a first-in first-out order.
#     
        # The *env* parameter is the :class:`~simpy.core.Environment` instance the
        # container is bound to.
#     
        # """
        # def __init__(self, env, capacity=float('inf')):
            # if capacity <= 0:
                # raise ValueError('"capacity" must be > 0.')
#     
            # super(Store, self).__init__(env, capacity)
#     
            # self.items = []
            # """List of the items available in the store."""
#     
        # put = BoundClass(StorePut)
        # """Request to put *item* into the store."""
#     
        # get = BoundClass(StoreGet)
        # """Request to get an *item* out of the store."""
#     
        # def _do_put(self, event):
            # if len(self.items) < self._capacity:
                # self.items.append(event.item)
                # event.succeed()
#     
        # def _do_get(self, event):
            # if self.items:
                # event.succeed(self.items.pop(0))
#     
#     
    # class FilterStore(Store):
        # """Resource with *capacity* slots for storing arbitrary _objects supporting
        # filtered get requests. Like the :class:`Store`, the *capacity* is unlimited
        # by default and _objects are put and retrieved from the store in a first-in
        # first-out order.
#     
        # Get requests can be customized with a filter function to only trigger for
        # items for which said filter function returns ``True``.
#     
        # .. note::
#     
            # In contrast to :class:`Store`, get requests of a :class:`FilterStore`
            # won't necessarily be triggered in the same order they were issued.
#     
            # *Example:* The store is empty. *Process 1* tries to get an item of type
            # *a*, *Process 2* an item of type *b*. Another process puts one item of
            # type *b* into the store. Though *Process 2* made his request after
            # *Process 1*, it will receive that new item because *Process 1* doesn't
            # want it.
#     
        # """
#     
        # put = BoundClass(StorePut)
        # """Request a to put *item* into the store."""
#     
        # get = BoundClass(FilterStoreGet)
        # """Request a to get an *item*, for which *filter* returns ``True``, out of
        # the store."""
#     
        # def _do_get(self, event):
            # for item in self.items:
                # if event.filter(item):
                    # self.items.remove(item)
                    # event.succeed(item)
                    # break
            # return True
# 
#             
# 
#     
#     
    # class EmptySchedule(Exception):
        # """Thrown by an :class:`Environment` if there are no further events to be
        # processed."""
        # pass
#     
#     
    # class StopSimulation(Exception):
        # """Indicates that the simulation should stop now."""
#     
        # @classmethod
        # def callback(cls, event):
            # """Used as callback in :meth:`BaseEnvironment.run()` to stop the
            # simulation when the *until* event occurred."""
            # if event.ok:
                # raise cls(event.value)
            # else:
                # raise event.value
#     
#     
    # class BaseEnvironment(_object):
        # """Base class for event processing environments.
#     
        # An implementation must at least provide the means to access the current
        # time of the environment (see :attr:`now`) and to schedule (see
        # :meth:`schedule()`) events as well as processing them (see :meth:`step()`.
#     
        # The class is meant to be subclassed for different execution environments.
        # For example, SimPy defines a :class:`Environment` for simulations with
        # a virtual time and and a :class:`~simpy.rt.RealtimeEnvironment` that
        # schedules and executes events in real (e.g., wallclock) time.
#     
        # """
        # @property
        # def now(self):
            # """The current time of the environment."""
            # raise NotImplementedError(self)
#     
        # @property
        # def active_process(self):
            # """The currently active process of the environment."""
            # raise NotImplementedError(self)
#     
        # def schedule(self, event, priority=NORMAL, delay=0):
            # """Schedule an *event* with a given *priority* and a *delay*.
#     
            # There are two default priority values, :data:`~simpy.events.URGENT` and
            # :data:`~simpy.events.NORMAL`.
#     
            # """
            # raise NotImplementedError(self)
#     
        # def step(self):
            # """Processes the next event."""
            # raise NotImplementedError(self)
#     
        # def run(self, until=None):
            # """Executes :meth:`step()` until the given criterion *until* is met.
#     
            # - If it is ``None`` (which is the default), this method will return
              # when there are no further events to be processed.
#     
            # - If it is an :class:`~simpy.events._Event`, the method will continue
              # stepping until this event has been triggered and will return its
              # value.  Raises a :exc:`RuntimeError` if there are no further events
              # to be processed and the *until* event was not triggered.
#     
            # - If it is a number, the method will continue stepping
              # until the environment's time reaches *until*.
#     
            # """
            # if until is not None:
                # if not isinstance(until, _Event):
                    # # Assume that *until* is a number if it is not None and
                    # # not an event.  Create a Timeout(until) in this case.
                    # at = float(until)
#     
                    # if at <= self.now:
                        # raise ValueError('until(=%s) should be > the current '
                                         # 'simulation time.' % at)
#     
                    # # Schedule the event with before all regular timeouts.
                    # until = _Event(self)
                    # until.ok = True
                    # until._value = None
                    # self.schedule(until, URGENT, at - self.now)
#     
                # elif until.callbacks is None:
                    # # Until event has already been processed.
                    # return until.value
#     
                # until.callbacks.append(StopSimulation.callback)
#     
            # try:
                # while True:
                    # self.step()
            # except StopSimulation as exc:
                # return exc.args[0]  # == until.value
            # except EmptySchedule:
                # if until is not None:
                    # # @ FIXED ASSERTION ERROR
                    # try:
                        # not until.triggered
                    # except:
                        # pass
                    # raise RuntimeError('No scheduled events left but "until" '
                                       # 'event was not triggered: %s' % until)
#     
        # def exit(self, value=None):
            # """Stop the current process, optionally providing a ``value``.
#     
            # This is a convenience function provided for Python versions prior to
            # 3.3. From Python 3.3, you can instead use ``return value`` in
            # a process.
#     
            # """
            # raise StopIteration(value)
#     
#     
    # class Environment(BaseEnvironment):
        # """Execution environment for an event-based simulation. The passing of time
        # is simulated by stepping from event to event.
#     
        # You can provide an *initial_time* for the environment. By default, it
        # starts at ``0``.
#     
        # This class also provides aliases for common event types, for example
        # :attr:`process`, :attr:`timeout` and :attr:`event`.
#     
        # """
        # def __init__(self, initial_time=0):
            # self._now = initial_time
            # self._queue = []  # The list of all currently scheduled events.
            # self._eid = count()  # Counter for event IDs
            # self._active_proc = None
#     
            # # Bind all BoundClass instances to "self" to improve performance.
            # BoundClass.bind_early(self)
#     
        # @property
        # def now(self):
            # """The current simulation time."""
            # return self._now
#     
        # @property
        # def active_process(self):
            # """The currently active process of the environment."""
            # return self._active_proc
#     
        # process = BoundClass(Process)
        # timeout = BoundClass(Timeout)
        # event = BoundClass(_Event)
        # all_of = BoundClass(AllOf)
        # any_of = BoundClass(AnyOf)
#     
        # def schedule(self, event, priority=NORMAL, delay=0):
            # """Schedule an *event* with a given *priority* and a *delay*."""
            # heappush(self._queue,
                     # (self._now + delay, priority, next(self._eid), event))
#     
        # def peek(self):
            # """Get the time of the next scheduled event. Return
            # :data:`~simpy.core.Infinity` if there is no further event."""
            # try:
                # return self._queue[0][0]
            # except IndexError:
                # return Infinity
#     
        # def step(self):
            # """Process the next event.
#     
            # Raise an :exc:`EmptySchedule` if no further events are available.
#     
            # """
            # try:
                # self._now, _, _, event = heappop(self._queue)
            # except IndexError:
                # raise EmptySchedule()
#     
            # # Process callbacks of the event. Set the events callbacks to None
            # # immediately to prevent concurrent modifications.
            # callbacks, event.callbacks = event.callbacks, None
            # for callback in callbacks:
                # callback(event)
#     
            # if not event.ok and not hasattr(event, 'defused'):
                # # The event has failed and has not been defused. Crash the
                # # environment.
                # # Create a copy of the failure exception with a new traceback.
                # exc = type(event._value)(*event._value.args)
                # exc.__cause__ = event._value
                # raise exc
                

    
            
init python:

    def set_font_color(s, color):
        """
        @param: color: should be supplied as a string! Not as a variable!
        Sets font color duting interpolation.
        """
        return "".join(["{color=[%s]}" % color, "{}".format(s), "{/color}"])
        
    class BuildingRelay(object):
        """An upgrade has a limited number of rooms to
        run jobs in parallel.
        
        Single Customer handling...
        
        @ TODO: I thinks this bit should be assigned to Building Upgrades!
    
        Clients have to have to request one of the rooms. When they got one, they
        can start the job processes and wait for it to finish (which
        takes jobtime descrete units).
        """
        def __init__(self, env):
            self.env = env
            
            # Bad way of handing Brothel Upgrade:
            self.building = object()
            self.building.res = simpy.Resource(env, 2)
            self.building.time = 5
            self.building.cap = 2
            
            self.sc = object()
            self.sc.res = simpy.Resource(env, 10)
            self.sc.time = 10 # Time it takes to clear one client.
            self.sc.cap = 10 # Capacity
            self.sc.cash = 0
            
        def building_client_dispatcher(self, evn, client):
            """The client_dispatcher process arrives at the building
            and requests a a room.
        
            It then starts the washing process, waits for it to finish and
            leaves to never come back...
            """
            with self.building.res.request() as request:
                yield request
                
                while store.nd_chars:
                    
                    # Here we should attempt to find the best match for the client!
                    store.char = store.nd_chars.pop()
                    
                    # First check is the char is still well and ready:
                    if not check_char(store.char):
                        if store.char in store.nd_chars:
                            store.nd_chars.remove(store.char)
                        temp = set_font_color('{} is done with this job for the day.'.format(store.char.name), "aliceblue")
                        store.building.nd_events_report.append(temp)
                        continue
                    
                    # We to make sure that the girl is willing to do the job:
                    temp = store.char.action.id
                    if not store.char.action.check_occupation(store.char):
                        if store.char in store.nd_chars:
                            store.nd_chars.remove(store.char)
                        temp = set_font_color('{} is not willing to do {}.'.format(store.char.name, temp), "red")
                        store.building.nd_events_report.append(temp)
                        continue
                        
                        # All is well and we create the event
                    temp = "{} and {} enter the room at {}".format(client.name, char.name, env.now)
                    store.building.nd_events_report.append(temp)
                    
                    yield env.process(self.run_building_job(client, char))
                    
                    temp = "{} leaves at {}".format(client.name, env.now)
                    store.building.nd_events_report.append(temp)
                    return
                    
                # devlog.info("Clients: {}, Girls: {}".format(len(store.nd_clients), len(store.nd_girls)))    
                temp = "No girls were availible for {}".format(client.name)
                store.building.nd_events_report.append(temp)
                
                env.process(self.kick_client(client))
                
        def sc_client_dispatcher(self, evn, client):
            """The client_dispatcher process arrives at the building
            and requests a a room.
        
            It then starts the washing process, waits for it to finish and
            leaves to never come back...
            """
            with self.sc.res.request() as request:
                yield request
                
                # All is well and we create the event
                temp = "{} enters the Strip Club at {}".format(client.name, env.now)
                store.building.nd_events_report.append(temp)
                
                yield env.process(self.run_sc_job(client, char))
                
                temp = "{} leaves the Club at {}".format(client.name, env.now)
                store.building.nd_events_report.append(temp)
                # return
                    
                # devlog.info("Clients: {}, Girls: {}".format(len(store.nd_clients), len(store.nd_girls)))    
                # temp = "No girls were availible for {}".format(client.name)
                # store.building.nd_events_report.append(temp)
                # env.process(self.kick_client(client))
            
        def run_building_job(self, client, char):
            """
            This should be a job...
            """
            yield self.env.timeout(self.building.time)
            if config.debug:
                temp = "Debug: {} Brothel Resource in use!".format(set_font_color(self.building.res.count, "red"))
                store.building.nd_events_report.append(temp)
            
            temp = "{} and {} did their thing!".format(set_font_color(char.name, "pink"), client.name)
            store.building.nd_events_report.append(temp)
            store.client = client
            store.char = char
            char.action()
            # We return the char to the nd list
            
            store.nd_chars.insert(0, char)
            
        def run_sc_job(self, client, char):
            """
            This should be a job...
            """
            yield self.env.timeout(self.sc.time)
            self.sc.cash += 100
            if config.debug:
                temp = "Debug: {} Strip Club Resource currently in use/ Cash earned: {}!".format(set_font_color(self.sc.res.count, "red"), self.sc.cash)
                store.building.nd_events_report.append(temp)
            
            # temp = "{} and {} did their thing!".format(set_font_color(char.name, "pink"), client.name)
            # store.building.nd_events_report.append(temp)
            # store.client = client
            # store.char = char
            # char.action()
            # store.nd_clients.remove(store.client)
            # We return the char to the nd list
            # store.nd_chars.insert(0, char)
            
        def kick_client(self, client):
            """
            Gets rid of this client...
            """
            yield self.env.timeout(1)
            temp = "There is not much for the {} to do...".format(client.name)
            store.building.nd_events_report.append(temp)
            temp = "So {} leaves the hotel cursing...".format(client.name)
            store.building.nd_events_report.append(temp)
            # store.nd_clients.remove(store.client)
    
    def setup(env, end=40):
        """
        First attempt at making a jobs loop with SimPy!
        @param: We should draw end from the building.
        """
        # Create the building
        upgrade = BuildingRelay(env)
    
        # for i in xrange(2):
            # store.client = store.nd_clients.pop()
            # store.client.name = "Client {}".format(i)
            # # if self.room.
            # env.process(upgrade.building_client_dispatcher(env, store.client))
        # Create more clients while the simulation is running if such are availible...
        
        i = 0
        while store.nd_clients:
            if env.now + 5 <= end: # This is a bit off... should we decide which action should be taken first?
                if i > 4:
                    yield env.timeout(random.randint(1, 3))
                i += 1
                store.client = store.nd_clients.pop()
                store.client.name = "Client {}".format(i)
                
                # Register the fact that client arrived at the building:
                temp = '{} arrives at the {} at {}.'.format(client.name, store.building.name, env.now)
                store.building.nd_events_report.append(temp)
                
                # Take an action!
                # Must be moved to 
                whores = list(i for i in store.nd_chars if "SIW" in i.occupations)
                strippers = list(i for i in store.nd_chars if traits["Stripper"] in i.occupations)
                servers = list(i for i in store.nd_chars if "Server" in i.occupations)
                if upgrade.building.res.count < upgrade.building.cap and (store.nd_chars):
                    env.process(upgrade.building_client_dispatcher(env, store.client))
                elif upgrade.sc.res.count < upgrade.sc.cap:
                    env.process(upgrade.sc_client_dispatcher(env, store.client))
                else:
                    env.process(upgrade.kick_client(client))
            else:
                break


label temp_jobs_loop:
    $ tl.timer("Temp Jobs Loop")
    # Setup and start the simulation
    $ store.building.nd_events_report.append("\n\n")
    $ store.building.nd_events_report.append(set_font_color("===================", "lawngreen"))
    $ store.building.nd_events_report.append("{}".format(set_font_color("Starting the simulation:", "lawngreen")))
    $ store.building.nd_events_report.append("{}".format(set_font_color("Testing a Building with two rooms:", "lawngreen")))
    # $ random.seed(RANDOM_SEED)  # This helps reproducing the results
    
    # Create an environment and start the setup process
    $ env = simpy.Environment()
    $ env.process(setup(env, end=100))
    $ env.run(until=100)
    $ store.building.nd_events_report.append("{}".format(set_font_color("Ending the First Stage:", "red")))
    $ env.run(until=110)
    $ store.building.nd_events_report.append("{}".format(set_font_color("Ending the simulation:", "red")))
    $ store.building.nd_events_report.append("{}".format(set_font_color("===================", "red")))
    $ store.building.nd_events_report.append("\n\n")
    $ tl.timer("Temp Jobs Loop")
    
    return
    
label reg_H_event:
    $ chars["Hinata"].set_flag("event_to_interactions_10012adacx2134s", value={"label": "some_Hinata_label", "button_name": "Hinata Q", "condition": "True"})
    return
    
label some_Hinata_label:
    "Event Goes here..."
    "Don't forget to delete/change the flag one you're done!"
    $ chars["Hinata"].del_flag("event_to_interactions_10012adacx2134s")
    jump girl_interactions
