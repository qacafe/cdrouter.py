#
# Copyright (c) 2017 by QA Cafe.
# All Rights Reserved.
#

"""Module for constructing CDRouter Web API filters."""

import collections

class CDRouterFilterError(BaseException):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class Field(object):
    """Class for constructing CDRouter Web API filters.  Field objects can
    be passed to ``filter`` parameters to make constructing filters
    easier.

    The ``value`` parameter passed to Field methods is converted to a
    string using the builtin ``str`` function.  Bool values are
    additionally lowercased such that bool ``True`` becomes string
    ``'true'`` and ``False`` becomes string ``'false'``.  The Field
    methods ``contains``, ``contained_by`` and ``overlaps`` accept a
    variable number of values which are converted into a list in
    accordance with the API's syntax.  For example, the int values ``1, 2,
    3`` is converted to the string ``'{1,2,3}'`` and the string values
    ``'one', 'two', 'three'`` is converted to the string
    ``'{one,two,three}'``.

    Usage::

      from cdrouter.filters import Field as field
      # each pair of filters below are equivalent
      c.packages.list(filter=[
          field('id').eq(123),
          'id=123',
          #
          field('use_as_testlist').ne(True),
          'use_as_testlist!=true',
          #
          field('name').not_().match('^(foo|bar)$', ignorecase=True),
          'name!~*^(foo|bar)$',
          #
          field('tags').contains('foo', 'bar', 'baz'),
          'tags@>{foo,bar,baz}',
      ])

    See this_ page for more details on CDRouter Web API filters.

    .. _this: https://support.qacafe.com/cdrouter-web-api/overview/#filtering
    """

    def __init__(self, *args):
        if len(args) == 0:
            raise CDRouterFilterError('Filter must have at least one field')
        self.negate = False
        self.field = '.'.join(args)
        self.op = None
        self.negate_op = None
        self.value = None

    def __str__(self):
        if self.field is None:
            raise CDRouterFilterError('Filter field not set')
        if self.negate and self.negate_op is None:
            raise CDRouterFilterError('Filter negate operator not set')
        if not self.negate and self.op is None:
            raise CDRouterFilterError('Filter operator not set')
        if self.value is None:
            raise CDRouterFilterError('Filter value not set')
        op = self.op
        if self.negate:
            op = self.negate_op
        return '{}{}{}'.format(self.field, op, self.value)

    def _value(self, value):
        if isinstance(value, bool):
            return str(value).lower()
        return value

    def _array_value(self, value):
        value = self._value(value)
        if not isinstance(value, collections.Iterable):
            value = [value]
        return '{{{}}}'.format(','.join([str(v) for v in value]))

    def not_(self):
        """Negate the filter.  Not supported by ``contains``, ``contained_by``
        or ``overlaps`` methods.

        :return: :class:`filters.Field <filters.Field>` object
        :rtype: filters.Field

        """
        self.negate = True
        return self

    def eq(self, value):
        """Construct an equal to (``=``) filter.

        :param value: Filter value
        :return: :class:`filters.Field <filters.Field>` object
        :rtype: filters.Field
        """
        self.op = '='
        self.negate_op = '!='
        self.value = self._value(value)
        return self

    def ne(self, value):
        """Construct a not equal to (``!=``) filter.

        :param value: Filter value
        :return: :class:`filters.Field <filters.Field>` object
        :rtype: filters.Field
        """
        self.op = '!='
        self.negate_op = '='
        self.value = self._value(value)
        return self

    def gt(self, value):
        """Construct a greater than (``>``) filter.

        :param value: Filter value
        :return: :class:`filters.Field <filters.Field>` object
        :rtype: filters.Field
        """
        self.op = '>'
        self.negate_op = '<='
        self.value = self._value(value)
        return self

    def ge(self, value):
        """Construct a greater than or equal to (``>=``) filter.

        :param value: Filter value
        :return: :class:`filters.Field <filters.Field>` object
        :rtype: filters.Field
        """
        self.op = '>='
        self.negate_op = '<'
        self.value = self._value(value)
        return self

    def lt(self, value):
        """Construct a less than (``<``) filter.

        :param value: Filter value
        :return: :class:`filters.Field <filters.Field>` object
        :rtype: filters.Field
        """
        self.op = '<'
        self.negate_op = '>='
        self.value = self._value(value)
        return self

    def le(self, value):
        """Construct a less than or equal to (``<=``) filter.

        :param value: Filter value
        :return: :class:`filters.Field <filters.Field>` object
        :rtype: filters.Field
        """
        self.op = '<='
        self.negate_op = '>'
        self.value = self._value(value)
        return self

    def match(self, value, ignorecase=False):
        """Construct a regexp match (``~``) filter.  Combine with ``not_`` method to construct a negative regexp match (``!~``) filter.

        :param value: Filter value
        :param ignorecase: If bool `True`, make match case insensitive (``~*``, ``!~*``)
        :return: :class:`filters.Field <filters.Field>` object
        :rtype: filters.Field
        """
        if not ignorecase:
            self.op = '~'
            self.negate_op = '!~'
        else:
            self.op = '~*'
            self.negate_op = '!~*'
        self.value = self._value(value)
        return self

    def contains(self, *args):
        """Construct an array contains (``@>``) filter.

        :param args: Filter values
        :return: :class:`filters.Field <filters.Field>` object
        :rtype: filters.Field
        """
        self.op = '@>'
        self.negate_op = None
        self.value = self._array_value(args)
        return self

    def contained_by(self, *args):
        """Construct an array contained by (``<@``) filter.

        :param args: Filter values
        :return: :class:`filters.Field <filters.Field>` object
        :rtype: filters.Field
        """
        self.op = '<@'
        self.negate_op = None
        self.value = self._array_value(args)
        return self

    def overlaps(self, *args):
        """Construct an array overlaps (``&&``) filter.

        :param args: Filter values
        :return: :class:`filters.Field <filters.Field>` object
        :rtype: filters.Field
        """
        self.op = '&&'
        self.negate_op = None
        self.value = self._array_value(args)
        return self
