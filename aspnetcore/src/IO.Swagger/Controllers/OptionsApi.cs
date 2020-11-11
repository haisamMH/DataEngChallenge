/*
 * Dilmah-Admin-BFF
 *
 * No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)
 *
 * OpenAPI spec version: 1.0.0
 * 
 * Generated by: https://github.com/swagger-api/swagger-codegen.git
 */
using System;
using System.Collections.Generic;
using Microsoft.AspNetCore.Mvc;
using Swashbuckle.AspNetCore.Annotations;
using Swashbuckle.AspNetCore.SwaggerGen;
using Newtonsoft.Json;
using System.ComponentModel.DataAnnotations;
using IO.Swagger.Attributes;

using Microsoft.AspNetCore.Authorization;
using IO.Swagger.Models;

namespace IO.Swagger.Controllers
{ 
    /// <summary>
    /// 
    /// </summary>
    [ApiController]
    public class OptionsApiController : ControllerBase
    { 
        /// <summary>
        /// get option by id
        /// </summary>
        /// <param name=""></param>
        /// <response code="200">success</response>
        [HttpGet]
        [Route("/options/{code}")]
        [ValidateModelState]
        [SwaggerOperation("OptionsCodeGet")]
        public virtual IActionResult OptionsCodeGet([FromRoute][Required] )
        { 
            //TODO: Uncomment the next line to return response 200 or use other options such as return this.NotFound(), return this.BadRequest(..), ...
            // return StatusCode(200);

            throw new NotImplementedException();
        }

        /// <summary>
        /// Get all options
        /// </summary>
        /// <response code="200">success</response>
        [HttpGet]
        [Route("/options")]
        [ValidateModelState]
        [SwaggerOperation("OptionsGet")]
        public virtual IActionResult OptionsGet()
        { 
            //TODO: Uncomment the next line to return response 200 or use other options such as return this.NotFound(), return this.BadRequest(..), ...
            // return StatusCode(200);

            throw new NotImplementedException();
        }

        /// <summary>
        /// create an option
        /// </summary>
        /// <response code="200">success</response>
        [HttpPost]
        [Route("/options")]
        [ValidateModelState]
        [SwaggerOperation("OptionsPost")]
        public virtual IActionResult OptionsPost()
        { 
            //TODO: Uncomment the next line to return response 200 or use other options such as return this.NotFound(), return this.BadRequest(..), ...
            // return StatusCode(200);

            throw new NotImplementedException();
        }
    }
}