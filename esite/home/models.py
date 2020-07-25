from django.http import HttpResponse
from django.db import models
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.admin.edit_handlers import (
    PageChooserPanel,
    TabbedInterface,
    ObjectList,
    InlinePanel,
    StreamFieldPanel,
    MultiFieldPanel,
    FieldPanel,
)
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField
from modelcluster.fields import ParentalKey

from esite.colorfield.fields import ColorField, ColorAlphaField
from esite.colorfield.blocks import ColorBlock, ColorAlphaBlock, GradientColorBlock

from esite.api.helpers import register_streamfield_block

from esite.api.models import (
    GraphQLForeignKey,
    GraphQLField,
    GraphQLStreamfield,
    GraphQLImage,
    GraphQLString,
    GraphQLCollection,
    GraphQLEmbed,
    GraphQLSnippet,
    GraphQLBoolean,
    GraphQLSnippet,
)

# Create your homepage related models here.


@register_snippet
class HomeButton(models.Model):
    button_title = models.CharField(null=True, blank=False, max_length=255)
    # button_id = models.CharField(null=True, blank=True, max_length=255)
    # button_class = models.CharField(null=True, blank=True, max_length=255)
    button_embed = models.CharField(null=True, blank=True, max_length=255)
    button_link = models.URLField(null=True, blank=True)
    button_page = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [
        FieldPanel("button_title"),
        FieldPanel("button_embed"),
        FieldPanel("button_link"),
        PageChooserPanel("button_page"),
    ]

    def __str__(self):
        return self.button_title


# > Headers
@register_streamfield_block
class _H_HomeBannerBlock(blocks.StructBlock):
    head = blocks.CharBlock(
        null=True,
        blank=False,
        classname="full title",
        help_text="The bold header text at the frontpage slider",
    )

    graphql_fields = [
        GraphQLString("head"),
    ]


@register_streamfield_block
class _H_HomeFullBlock(blocks.StructBlock):
    head = blocks.CharBlock(blank=True, classname="full title", icon="title")

    graphql_fields = [
        GraphQLString("head"),
    ]


# Sections
@register_streamfield_block
class HomeAboutPagesBlock(blocks.StructBlock):
    blink = blocks.CharBlock(blank=True, classname="full")
    use_image = blocks.BooleanBlock(
        default=False, help_text="Use picture instead of blink", required=False
    )
    image = ImageChooserBlock(required=False, classname="full")
    boxes = blocks.StreamBlock(
        [
            (
                "title",
                blocks.CharBlock(
                    null=True, blank=True, classname="full title", icon="title"
                ),
            ),
            ("content", blocks.RichTextBlock(null=True, blank=True, classname="full")),
        ],
        null=True,
        blank=False,
    )

    graphql_fields = [
        GraphQLStreamfield("boxes"),
        GraphQLString("blink"),
        GraphQLBoolean("use_image"),
        GraphQLImage("image"),
    ]


@register_streamfield_block
class _S_HomeAboutBlock(blocks.StructBlock):
    pages = blocks.StreamBlock(
        [("page", HomeAboutPagesBlock(null=True, blank=False, icon="cogs"))],
        null=True,
        blank=False,
    )

    graphql_fields = [
        GraphQLStreamfield("pages"),
    ]


@register_streamfield_block
class _S_HomeMotdBlock(blocks.StructBlock):
    modt = blocks.CharBlock(max_length=16, default="Sky's The Limit", classname="full")

    graphql_fields = [
        GraphQLString("modt"),
    ]


@register_streamfield_block
class HomeSharinganTeamMemberBlock(blocks.StructBlock):
    pic = ImageChooserBlock(blank=True, classname="full")
    name = blocks.CharBlock(blank=True, max_length=16, default="", classname="full")
    description = blocks.CharBlock(max_length=128, default="", classname="full")

    graphql_fields = [
        GraphQLImage("pic"),
        GraphQLString("name"),
        GraphQLString("description"),
    ]


@register_streamfield_block
class _S_HomeSharinganBlock(blocks.StructBlock):
    show_projects = blocks.BooleanBlock(
        default=True,
        help_text="Whether sh1, sh2, sh3 will be shown on this block",
        required=False,
    )
    sharingan1 = blocks.RichTextBlock(null=True, blank=False, classname="full")
    sharingan2 = blocks.RichTextBlock(null=True, blank=False, classname="full")
    sharingan3 = blocks.RichTextBlock(null=True, blank=False, classname="full")

    show_team = blocks.BooleanBlock(
        default=False,
        help_text="Whether the team will be shown on this block",
        required=False,
    )
    nyan_title = blocks.CharBlock(max_length=16, default="The Team", classname="full")
    members = blocks.StreamBlock(
        [("member", HomeSharinganTeamMemberBlock(null=True, blank=False, icon="user"))],
        blank=False,
    )

    graphql_fields = [
        GraphQLBoolean("show_projects"),
        GraphQLString("sharingan1"),
        GraphQLString("sharingan2"),
        GraphQLString("sharingan3"),
        GraphQLBoolean("show_team"),
        GraphQLString("nyan_title"),
        GraphQLStreamfield("members"),
    ]


@register_streamfield_block
class HomeCommunityAdminMemberBlock(blocks.StructBlock):
    pic = ImageChooserBlock(blank=True, classname="full")
    name = blocks.CharBlock(blank=True, max_length=16, default="", classname="full")
    description = blocks.CharBlock(max_length=128, default="", classname="full")

    graphql_fields = [
        GraphQLImage("pic"),
        GraphQLString("name"),
        GraphQLString("description"),
    ]


@register_streamfield_block
class HomeCommunityAdminMrowBlock(blocks.StructBlock):
    members = blocks.StreamBlock(
        [
            (
                "member",
                HomeCommunityAdminMemberBlock(null=True, blank=False, icon="user"),
            )
        ],
        required=False,
    )

    graphql_fields = [
        GraphQLStreamfield("members"),
    ]


@register_streamfield_block
class HomeCommunityAdminBlock(blocks.StructBlock):
    show_admins = blocks.BooleanBlock(
        default=True,
        help_text="Whether the admins will be shown on this block",
        required=False,
    )
    title = blocks.CharBlock(max_length=16, default="Admins", classname="full")
    mrows = blocks.StreamBlock(
        [("mrow", HomeCommunityAdminMrowBlock(blank=False, null=True, icon="group"))],
        required=False,
    )

    graphql_fields = [
        GraphQLBoolean("show_admins"),
        GraphQLString("admins_title"),
        GraphQLStreamfield("mrows"),
    ]


@register_streamfield_block
class HomeCommunityModMemberBlock(blocks.StructBlock):
    pic = ImageChooserBlock(blank=True, classname="full")
    name = blocks.CharBlock(blank=True, max_length=16, default="", classname="full")

    graphql_fields = [GraphQLImage("pic"), GraphQLString("name")]


@register_streamfield_block
class HomeCommunityModMrowBlock(blocks.StructBlock):
    members = blocks.StreamBlock(
        [("member", HomeCommunityModMemberBlock(null=True, blank=False, icon="user"))],
        required=False,
    )

    graphql_fields = [
        GraphQLStreamfield("members"),
    ]


@register_streamfield_block
class HomeCommunityModBlock(blocks.StructBlock):
    show_mods = blocks.BooleanBlock(
        default=True,
        help_text="Whether the mods will be shown on this block",
        required=False,
    )
    title = blocks.CharBlock(max_length=16, default="Mods", classname="full")
    mrows = blocks.StreamBlock(
        [("mrow", HomeCommunityModMrowBlock(blank=False, null=True, icon="group"))],
        required=False,
    )

    graphql_fields = [
        GraphQLBoolean("show_mods"),
        GraphQLString("mods_title"),
        GraphQLStreamfield("mrows"),
    ]


@register_streamfield_block
class _S_HomeCommunityBlock(blocks.StructBlock):
    admins = blocks.StreamBlock(
        [("admin", HomeCommunityAdminBlock(null=True, blank=False, icon="group"))]
    )
    mods = blocks.StreamBlock(
        [("mod", HomeCommunityModBlock(null=True, blank=False, icon="group"))]
    )

    graphql_fields = [GraphQLStreamfield("admins"), GraphQLStreamfield("mods")]


@register_streamfield_block
class _S_HomeSpaceshipBlock(blocks.StructBlock):
    pass


@register_streamfield_block
class _S_HomeGalleryBlock(blocks.StructBlock):
    title = blocks.CharBlock(blank=True, classname="full")
    gallery = blocks.StreamBlock(
        [("image", ImageChooserBlock(blank=True, classname="full")),]
    )

    graphql_fields = [
        GraphQLString("title"),
        GraphQLStreamfield("gallery"),
        GraphQLImage("image"),
    ]


@register_streamfield_block
class _S_HomeCodeBlock(blocks.StructBlock):
    code = blocks.RawHTMLBlock(blank=True, classname="full")

    graphql_fields = [
        GraphQLString("code"),
    ]


# > Homepage
class HomePage(Page):
    headers = StreamField(
        [
            ("h_banner", _H_HomeBannerBlock(null=True, blank=False, icon="title")),
            ("h_full", _H_HomeFullBlock(null=True, blank=False, icon="title")),
            (
                "h_code",
                blocks.RawHTMLBlock(
                    null=True, blank=True, classname="full", icon="code"
                ),
            ),
        ],
        null=True,
        blank=False,
    )

    sections = StreamField(
        [
            ("s_about", _S_HomeAboutBlock(null=True, blank=False, icon="radio-empty")),
            ("s_modt", _S_HomeMotdBlock(null=True, blank=False, icon="pilcrow")),
            ("s_sharingan", _S_HomeSharinganBlock(null=True, blank=False, icon="view")),
            (
                "s_community",
                _S_HomeCommunityBlock(null=True, blank=False, icon="group"),
            ),
            ("s_spaceship", _S_HomeSpaceshipBlock(null=True, blank=False, icon="pick")),
            ("s_gallery", _S_HomeGalleryBlock(null=True, blank=False, icon="grip")),
            ("s_code", _S_HomeCodeBlock(null=True, blank=False, icon="code")),
        ],
        null=True,
        blank=False,
    )

    # header = StreamField([
    #      ('hbanner', blocks.StructBlock([
    #        ('banner', blocks.CharBlock(blank=True, classname="full title", icon='title'))
    #      ], required=False, icon='bold')),
    #
    #      ('hfull', blocks.StructBlock([
    #        ('full', blocks.CharBlock(blank=True, classname="full title", icon='title'))
    #      ], required=False, icon='placeholder')),
    #
    #      ('hcode', blocks.StructBlock([
    #        ('code', blocks.RawHTMLBlock(blank=True, classname="full"))
    #      ], icon='code'))
    #    ], blank=True)

    #    article = StreamField([
    #      ('aabout', blocks.StructBlock([
    #        ('about_pages', blocks.StreamBlock([
    #          ('about', blocks.StructBlock([
    #            ('blink', blocks.CharBlock(blank=True, classname="full")),
    #            ('use_image', blocks.BooleanBlock(default=False, help_text="Use picture instead of blink", required=False, classname="full")),
    #            ('image', ImageChooserBlock(required=False, classname="full")),
    #            ('boxes', blocks.StreamBlock([
    #              ('title', blocks.CharBlock(blank=True, classname="full title", icon='title')),
    #              ('content', blocks.RichTextBlock(blank=True, features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'embed', 'link', 'document-link', 'image'], classname="full"))
    #            ]))
    #          ], icon='doc-full'))
    #        ], icon='cogs')),
    #      ], icon='radio-empty')),
    #
    #      ('amotd', blocks.StructBlock([
    #        ('modt', blocks.CharBlock(max_length=16, default="Sky's The Limit", classname="full")),
    #      ], icon='pilcrow')),
    #
    #      ('asharingan', blocks.StructBlock([
    #        ('sharingan', blocks.StructBlock([
    #          ('show_projects', blocks.BooleanBlock(default=True, help_text="Whether sh1, sh2, sh3 will be shown on this block", required=False, classname="full")),
    #          ('sharingan_1', blocks.RichTextBlock(default="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'embed', 'link', 'document-link', 'image'], classname="full")),
    #          ('sharingan_2', blocks.RichTextBlock(default="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'embed', 'link', 'document-link', 'image'], classname="full")),
    #          ('sharingan_3', blocks.RichTextBlock(default="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ol', 'ul', 'hr', 'embed', 'link', 'document-link', 'image'], classname="full")),
    #        ])),
    #        ('team', blocks.StructBlock([
    #          ('show_team', blocks.BooleanBlock(default=False, help_text="Whether the team will be shown on this block", required=False, classname="full")),
    #          ('nyan_titel', blocks.CharBlock(max_length=16, default="The Team", classname="full")),
    #          ('members', blocks.StreamBlock([
    #            ('member', blocks.StructBlock([
    #              ('pic', ImageChooserBlock(blank=True, classname="full")),
    #              ('name', blocks.CharBlock(blank=True, max_length=16, default="", classname="full")),
    #              ('description', blocks.CharBlock(max_length=128, default="", classname="full"))
    #            ], icon='user'))
    #          ], required=False))
    #        ]))
    #      ], icon='view')),
    #
    #      ('acommunity', blocks.StructBlock([
    #        ('admins', blocks.StructBlock([
    #          ('show_admins', blocks.BooleanBlock(default=True, help_text="Whether the admins will be shown on this block", required=False, classname="full")),
    #          ('admins_titel', blocks.CharBlock(max_length=16, default="Admins", classname="full")),
    #          ('members', blocks.StreamBlock([
    #            ('mrow', blocks.StreamBlock([
    #              ('member', blocks.StructBlock([
    #                ('pic', ImageChooserBlock(blank=True, classname="full")),
    #                ('name', blocks.CharBlock(blank=True, max_length=16, default="", classname="full")),
    #                ('description', blocks.CharBlock(max_length=128, default="", classname="full"))
    #              ], icon='user'))
    #            ], icon='group'))
    #          ], required=False))
    #        ])),
    #        ('mods', blocks.StructBlock([
    #          ('show_mods', blocks.BooleanBlock(default=True, help_text="Whether the mods will be shown on this block", required=False, classname="full")),
    #          ('mods_titel', blocks.CharBlock(max_length=16, default="Mods", classname="full")),
    #          ('members', blocks.StreamBlock([
    #            ('mrow', blocks.StreamBlock([
    #              ('member', blocks.StructBlock([
    #                ('pic', ImageChooserBlock(blank=True, classname="full")),
    #                ('name', blocks.CharBlock(blank=True, max_length=16, default="", classname="full"))
    #              ], icon='user'))
    #            ], icon='group'))
    #          ], required=False))
    #        ]))
    #      ], icon='group')),
    #
    #      ('aspaceship', blocks.StructBlock([
    #      ], icon='pick')),
    #
    #      ('agallery', blocks.StructBlock([
    #        ('title', blocks.CharBlock(blank=True, classname="full")),
    #        ('gallery', blocks.StreamBlock([
    #          ('image', ImageChooserBlock(blank=True, classname="full")),
    #        ]))
    #      ], icon='grip')),
    #
    #      ('acode', blocks.StructBlock([
    #        ('code', blocks.RawHTMLBlock(blank=True, classname="full"))
    #      ], icon='code'))
    #    ], blank=True)

    main_content_panels = [StreamFieldPanel("headers"), StreamFieldPanel("sections")]

    graphql_fields = [
        GraphQLStreamfield("headers"),
        GraphQLStreamfield("sections"),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(Page.content_panels + main_content_panels, heading="Main"),
            ObjectList(
                Page.promote_panels + Page.settings_panels,
                heading="Settings",
                classname="settings",
            ),
        ]
    )


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast

